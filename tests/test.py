import datetime
import os
import unittest

from mefipy import parse
from tagpage import tagpage_posts

files_directory = os.path.join(os.path.dirname(__file__), "data")

class TestTagPageParsing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(files_directory, "tagpage.html")) as tagpage:
            cls.parsed_posts = parse.parse_page_posts(tagpage.read())

    def test_num_posts_parsed(self):
        self.assertEqual(len(self.parsed_posts), len(tagpage_posts))
    
    def test_title_parsing(self):
        for post_index, parsed_post, compare_post in zip(range(1, len(self.parsed_posts)+1), self.parsed_posts, tagpage_posts):
            self.assertEqual(parsed_post.title, compare_post.title, msg=f"Failed title compare for post {post_index}")

    def test_date_posted_parsing(self):
        for post_index, parsed_post, compare_post in zip(range(1, len(self.parsed_posts)+1), self.parsed_posts, tagpage_posts):
            self.assertEqual(parsed_post.date_posted, compare_post.date_posted, msg=f"Failed date posted compare for post {post_index}")

    def test_post_link_parsing(self):
        for post_index, parsed_post, compare_post in zip(range(1, len(self.parsed_posts)+1), self.parsed_posts, tagpage_posts):
            self.assertEqual(parsed_post.date_posted, compare_post.date_posted, msg=f"Failed date posted compare for post {post_index}")

    def test_posted_by_link_parsing(self):
        for post_index, parsed_post, compare_post in zip(range(1, len(self.parsed_posts)+1), self.parsed_posts, tagpage_posts):
            self.assertEqual(parsed_post.posted_by_link, compare_post.posted_by_link, msg=f"Failed posted by link compare for post {post_index}")

    def test_posted_by_username_link_parsing(self):
        for post_index, parsed_post, compare_post in zip(range(1, len(self.parsed_posts)+1), self.parsed_posts, tagpage_posts):
            self.assertEqual(parsed_post.posted_by_username, compare_post.posted_by_username, msg=f"Failed posted by username compare for post {post_index}")

    def test_num_comments_parsing(self):
        for post_index, parsed_post, compare_post in zip(range(1, len(self.parsed_posts)+1), self.parsed_posts, tagpage_posts):
            self.assertEqual(parsed_post.num_comments, compare_post.num_comments, msg=f"Failed num comments compare for post {post_index}")

    def test_content_parsing(self):
        for post_index, parsed_post, compare_post in zip(range(1, len(self.parsed_posts)+1), self.parsed_posts, tagpage_posts):
            self.assertEqual(parsed_post.content, compare_post.content, msg=f"Failed content compare for post {post_index}")

if __name__ == '__main__':
    unittest.main()
