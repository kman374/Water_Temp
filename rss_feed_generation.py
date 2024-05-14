from feedgen.feed import FeedGenerator
import sqlite3

def generate_rss_feed():
    # Initialize FeedGenerator
    fg = FeedGenerator()
    fg.title('Water Temperature RSS Feed')
    fg.link(href='http://example.com', rel='alternate')
    fg.description('RSS feed for water temperature updates')

    # Connect to the SQLite database
    conn = sqlite3.connect('temperature.db')
    c = conn.cursor()

    # Query the database for the latest temperature data
    c.execute("SELECT temperature FROM temperature_data ORDER BY timestamp DESC LIMIT 1")
    latest_temperature = c.fetchone()

    if latest_temperature:
        # Add the latest temperature as an entry to the feed
        fe = fg.add_entry()
        fe.title('Temperature: ' + str(latest_temperature[0]))

    # Close database connection
    conn.close()

    # Generate RSS feed as string
    rss_feed = fg.rss_str(pretty=True)
    rss_feed_str = rss_feed.decode('utf-8')  # Decode bytes to string

    # Write RSS feed to file
    with open('temperature_feed.xml', 'w') as f:
        f.write(rss_feed_str)

# Generate RSS feed
generate_rss_feed()
