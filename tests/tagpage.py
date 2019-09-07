"""
The Pythonic representations we should get back after we parse our data/tagpage.html
"""
import datetime

from mefipy.parse import Post

# TODO: Our content should be what's INSIDE the div, not including the copy post div

tagpage_posts = [
    Post(
        title="I'm a Test Post",
        date_posted=datetime.date(2019, 8, 29),
        post_link='http://www.metafilter.com/12345/Im-a-Test-Post',
        posted_by_link='http://www.metafilter.com/user/55',
        posted_by_username='MeFite1',
        num_comments=38,
        content='<div class="copy post"><a href="test.com">Test</a><br/>\n\n</div>',
        tags=None),
    Post(
        title="“Test Post 2.”",
        date_posted=datetime.date(2019, 8, 10),
        post_link='http://www.metafilter.com/12346/Test-Post-2',
        posted_by_link='http://www.metafilter.com/user/91',
        posted_by_username='MeFite2',
        num_comments=96,
        content='<div class="copy post"><a href="http://loripsum.net/" target="_blank">Iam in altera philosophiae parte.</a> At iste non dolendi status non vocatur voluptas. <i>At certe gravius.</i> <b>Videsne, ut haec concinant?</b> <span class="smallcopy">[<a href="http://www.metafilter.com/12346/Test-Post-2" target="_self">more inside</a>]</span><br/>\n\n</div>',
        tags=None),
    Post(
        title="Test! Post! 3",
        date_posted=datetime.date(2019, 8, 9),
        post_link='http://www.metafilter.com/12347/Test-Post-3',
        posted_by_link='http://www.metafilter.com/user/27',
        posted_by_username='MeFite3',
        num_comments=411,
        content='<div class="copy post">Lorem ipsum dolor sit amet, consectetur adipiscing elit. <a href="http://loripsum.net/" target="_blank">Restinguet citius, si ardentem acceperit.</a> Cur id non ita fit? <a href="http://loripsum.net/" target="_blank">Quod totum contra est.</a> Paria sunt igitur. Tanta vis admonitionis inest in locis; <span class="smallcopy">[<a href="http://www.metafilter.com/12347/Test-Post-3" target="_self">more inside</a>]</span><br/>\n\n</div>',
        tags=None),
    Post(
        title="--TESTING PARSERS--",
        date_posted=datetime.date(2019, 8, 7),
        post_link='http://www.metafilter.com/12348/TESTING-PARSERS',
        posted_by_link='http://www.metafilter.com/user/36',
        posted_by_username='MeFite4',
        num_comments=1622,
        content='<div class="copy post"> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Equidem e Cn. Tollenda est atque extrahenda radicitus. Idem adhuc; <a href="http://loripsum.net/" target="_blank">Nos vero, inquit ille;</a> Tuo vero id quidem, inquam, arbitratu. Duo Reges: constructio interrete. <i>Quibusnam praeteritis?</i> Num quid tale Democritus? <span class="smallcopy">[<a href="http://www.metafilter.com/12348/TESTING-PARSERS" target="_self">more inside</a>]</span><br/>\n\n</div>',
        tags=None),
]
