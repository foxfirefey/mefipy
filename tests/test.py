import datetime
import os
import unittest

from mefipy import parse

files_directory = os.path.join(os.path.dirname(__file__), "data")

class TestTagPageParsing(unittest.TestCase):

    def test_post_parse(self):

        with open(os.path.join(files_directory, "tagpage.html")) as tagpage:
            posts = parse.parse_page_posts(tagpage.read())
        self.assertEqual(len(posts), 1)
        parsed_post = posts[0]
        compare_post = parse.Post(
            title="I'm a Test Post",
            date_posted=datetime.date(2019, 8, 29),
            post_link='http://www.metafilter.com/12345/Im-a-Test-Post',
            posted_by_link='http://www.metafilter.com/user/55',
            posted_by_username='MeFite1',
            num_comments=38,
            # TODO: Our content should be what's INSIDE the div, not 
            content='<div class="copy post"><a href="test.com">Test</a><br/>\n\n</div>',
            tags=None)
        self.assertEqual(parsed_post, compare_post)

if __name__ == '__main__':
    unittest.main()
