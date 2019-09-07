from collections import namedtuple
import datetime
import logging
import re
import sys

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

METAFILTER_URL = "https://www.metafilter.com/"
TAG_URL = "{METAFILTER_URL}/tags/{tag}?page={page}"
HTML_PARSER = "lxml"

Post = namedtuple('Post', ['title', 'date_posted', 'post_link', 'posted_by_link', 'posted_by_username', 'num_comments', 'content', 'tags'])
Comment = namedtuple('Comment', ['comment_link', 'posted_by_link', 'posted_by_username', 'timestamp', 'num_favorites', 'content'])

def comment_string(comment):
    return f"{comment.comment_link} by {comment.posted_by_username} on {comment.timestamp}"

def parse_page_post(post):
    try:    
        # the date it's posted, who by, and comments are all in the byline
        byline = post.find(attrs={"class": "postbyline"})
        # get the date
        post_date = re.search("on (?P<month>[A-Za-z]+) (?P<day>[0-9]+), (?P<year>[0-9]+) -", str(byline))
        if post_date:
            post_date = datetime.datetime.strptime(f"{post_date.group('month')}-{post_date.group('day')}-{post_date.group('year')}", "%b-%d-%Y").date()
        else:
            logger.error(f"No match for {str(byline)}", file=sys.stderr)
            return None
        # these are the first two links of the byline
        posted_by, comments = byline.find_all('a')[0:2]
        posted_by_link, posted_by_username = posted_by['href'], posted_by.text
        num_comments = int(comments.text.split(" ")[0])
    
        # our post title is the previous tag of this post   
        title = post.find_previous_sibling('h2', attrs={"class": "posttitle"})

        # Old can exist without titles, see: https://www.metafilter.com/20672/ in the plannedparenthood tag
        if title and len(title.a.contents):
            post_title = title.a.contents[0]
            post_link = title.a["href"]
        else:
            post_title = "{:%B %-d, %Y}".format(post_date)
            # honestly the comment link is the same thing
            post_link = comments['href']

        # remove the byline content; this will make it so our remainder post is just the content 
        byline.decompose()
        post_content = str(post)
    
        # no tags in this context
        return Post(post_title, post_date, post_link, posted_by_link, posted_by_username, num_comments, post_content, None)
    except Exception:
        logger.exception(f"Could not parse {post}")
        return None

def parse_page_posts(content):
    soup = BeautifulSoup(content, features=HTML_PARSER)
    return [parse_page_post(post) for post in soup.find_all(attrs={"class": "post"})]

def parse_post_copy(soup):
    """Post copy on comment pages is similar to but slighty different from blurbs on
    pages."""

    copy = soup.find(attrs={"class": "copy"})

    byline = soup.find(attrs={"class": "postbyline"})
    # our post link is in the head of the page
    canonical_link = soup.find('link', attrs={"rel": "canonical"})
    # their canonical link is currently http, we should link to https though
    post_link = canonical_link["href"].replace('http://', 'https://', 1)

    if not byline:
        logger.error(f"Could not find byline in {copy}")
        return None

    title = copy.find_previous_sibling('h1', attrs={"class": "posttitle"})

    # title is the part that comes before the <br /> tag
    post_title = title.contents[0]
    datetitle = title.find(attrs={"class": "smallcopy"})
    datetext = datetitle.contents[0]
    timetext = datetitle.contents[1].text

    post_date = datetime.datetime.strptime(f"{datetext} {timetext}", "%B %d, %Y %H:%M %p")

    posted_by = byline.find_all('a')[0]
    posted_by_link = posted_by['href']
    posted_by_username = posted_by.text
    num_comments = 0

    m = re.search("([0-9]+) comments total", byline.text)
    if m:
        num_comments = int(m.group(1))
    
    tags_div = soup.find('div', attrs={"id": "taglist"})
    tags_list = tags_div.find_all('a', attrs={"class": "taglink"})

    if tags_list:
        tags = [(tag_link["title"], tag_link["href"]) for tag_link in tags_list]
    else:
        tags = []

    # remove the byline content; this will make it so our remainder post is just the content 
    byline.decompose()
    post_content = str(copy)

    return Post(post_title, post_date, post_link, posted_by_link, posted_by_username, num_comments, post_content, tags)


def parse_post_comment(comment, post):
    # our byline is the last span present in the content
    byline = comment.find('span', attrs={"class": "smallcopy"})

    if not byline:
        logger.error(f"Could not find byline in {comment}")
        return None
  
    posted_by = None
    timestamp_link = None
    favorites = None

    # we can't rely on these links to be in any particular order
    # sometimes there's no favorites link
    # sometimes there's a staff link after the user link
    for byline_link in byline.find_all('a'):
        if "/user/" in byline_link["href"]:
            posted_by = byline_link
        elif "/favorited/" in byline_link["href"]:
            favorites = byline_link
        elif re.match("[0-9]{1,2}:[0-9]{2} (A|P)M", byline_link.text):
            timestamp_link = byline_link

    posted_by_link,  = posted_by['href'],
    # change our relative link to an absolute one
    comment_link = METAFILTER_URL + timestamp_link['href']
    posted_by_username = posted_by.text
    date_time = timestamp_link.text # 3:36 PM
   
    if not favorites:
        num_favorites = 0
    else:
        # "10 favorites"
        num_favorites = int(favorites.text.split(" ")[0])

    # our comment text has a date when a post is closed but not when a post is open?
    date_text = re.search(r"posted +by .+ +at +[0-9]+:[0-9]+ (A|P)M +on +(?P<month>[A-Za-z]+) +(?P<day>[0-9]+)(, +(?P<year>[0-9]+))?", byline.text)
    if not date_text:
        logger.error(f"No date text in {byline.text}")
        return None
    comment_date = datetime.datetime.strptime(f"{date_text.group('month')}-{date_text.group('day')}-{post.date_posted.year} {date_time}", "%B-%d-%Y %H:%M %p")

    # remove the byline content; this will make it so our remainder comment is just the content
    byline.decompose()
    comment_content = str(comment)

    return Comment(comment_link, posted_by_link, posted_by_username, comment_date, num_favorites, comment_content)

def parse_post_comments(content):
    soup = BeautifulSoup(content, features=HTML_PARSER)
    post = parse_post_copy(soup)

    # exclude <div class="comments" id="prevDiv"
    return post, [parse_post_comment(comment, post) for comment in soup.find_all('div', attrs={"class": "comments"}) if comment and "id" not in comment.attrs]


def parse_post_comments_between(content, start_timestamp, end_timestamp):
    soup = BeautifulSoup(content, features=HTML_PARSER)
    post = parse_post_copy(soup)

    # If we're not using datetimes for either our start or end, let's convert them
    if isinstance(start_timestamp, datetime.date):
        # turn into the start of the day
        start_timestamp = datetime.datetime(start_timestamp.year, start_timestamp.month, start_timestamp.day, 0, 0, 0, 0)
    if isinstance(end_timestamp, datetime.date):
        # turn into the end of the day
        end_timestamp = datetime.datetime(end_timestamp.year, end_timestamp.month, end_timestamp.day, 23, 59, 59, 999999)

    comments = []
    for comment in soup.find_all('div', attrs={"class": "comments"}):
        # exclude <div class="comments" id="prevDiv"
        # exclude <div class="comments" style="margin-bottom:22px;margin-top:10px;"> containing ads
        # exclude <div class="comments">You are not currently logged in.
        if "id" in comment.attrs or "style" in comment.attrs or comment.text.startswith("You are not currently logged in. Log in or create a new account to post comments."):
            continue
        comment = parse_post_comment(comment, post)
        if not comment:
            continue
        if comment.timestamp >= start_timestamp and comment.timestamp <= end_timestamp:
            comments.append(comment)
    
    return post, comments

def post_is_active(post, on_date, days_open=30):
    """Was this post active on the days after and before the given date range?"""

    if isinstance(on_date, datetime.datetime):
        on_date = datetime.date()

    post_activity_ends = post.date_posted + datetime.timedelta(days=30)

    return post_activity_ends >= on_date
    
def filter_active_posts(posts, on_date, days_open=30):
    """Given a list of posts, a date range, and the number of days open and what we consider to be "today",
       return only the posts that could have activity on them.  Err on the side of day after closing, because
       we can't time that exactly."""

    if isinstance(on_date, datetime.datetime):
        on_date = on_date.date()    

    return [post for post in posts if post_is_active(post, on_date, days_open=days_open)]

def get_tag_posts(tag, page=1):
    """Uses the requests library to post the first 50 posts that appear under a tag."""
    url = TAG_URL.format(tag=tag, page=page, METAFILTER_URL=METAFILTER_URL)
    result = requests.get(url)
    logger.info(f"Fetching {tag} page {page} [{url}]: {result}")
    return [post for post in parse_page_posts(result.content) if post]

def run_activity_summary(tags, start_date, end_date, report=sys.stdout, report_no_comments=False):
    logger.info("Fetching between {:%Y-%m-%d %I:%M %p} and {:%Y-%m-%d %I:%M %p} for {}".format(start_date, end_date, tags))
    print("Metafilter Politics Activity between {:%Y-%m-%d %I:%M %p} and {:%Y-%m-%d %I:%M %p}\n\n".format(start_date, end_date), file=report)

    posts = dict()
    for tag in tags:
        for post in filter_active_posts(get_tag_posts(tag), start_date):
            posts[post.post_link] = post
    # order our posts by date with the most recent first
    posts = sorted(list(posts.values()), key=lambda post: post.date_posted, reverse=True)
    
    print("<ul>", file=report)
    for post in posts:
        logger.info(f"Fetching {post.post_link}")
        result = requests.get(post.post_link)
        full_post, comments = parse_post_comments_between(result.content, start_date, end_date)

        if full_post.tags:
            tag_text = "<br /><small>Tags: " + ", ".join([tag[0] for tag in full_post.tags]) + "</small>"
        else:
            tag_text = ""

        if comments:
            print(f"""<li>[{full_post.date_posted.strftime("%Y-%m-%d")}] <a href="{full_post.post_link}">{post.title}</a> from {post.posted_by_username}: <a href="{comments[0].comment_link}">{len(comments)} new comments</a>{tag_text}</li>""", file=report)
        elif report_no_comments:
            continue
            print(f"""<li>[{full_post.date_posted.strftime("%Y-%m-%d")}] <a href="{full_post.post_link}">{post.title}</a> from {post.posted_by_username}: no new comments {tag_text}</li>""")
    print("</ul>", file=report)
