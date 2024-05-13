from feedgen.feed import FeedGenerator
import sqlite3

def generate_rss_feed():
    fg = FeedGenerator()
    fg.title('Water Temperature RSS Feed')
    fg.link(href='http://example.com', rel='alternate')
    fg.description('RSS feed for water temperature updates')

    conn = sqlite3.connect('temperature.db')
    c = conn.cursor()
    c.execute("SELECT temperature, timestamp FROM temperatures ORDER BY timestamp DESC LIMIT 10")
    rows = c.fetchall()

    for row in rows:
        temperature, timestamp = row
        fe = fg.add_entry()
        fe.title('Temperature: ' + str(temperature))
        fe.description('Recorded at: ' + timestamp)

    conn.close()

    rss_feed = fg.rss_str(pretty=True)
    rss_feed_str = rss_feed.decode('utf-8')  # Decode bytes to string
    with open('temperature_feed.xml', 'w') as f:
        f.write(rss_feed_str)

generate_rss_feed()
