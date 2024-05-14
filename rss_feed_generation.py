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
        # Set only the temperature as the title
        fe.title(str(latest_temperature[0])+'°F')

    # Close database connection
    conn.close()

    # Generate RSS feed as string
    rss_feed = fg.rss_str(pretty=True)
    rss_feed_str = rss_feed.decode('utf-8')  # Decode bytes to string

    # Extract only the title tag from the RSS feed
    start_tag = '<title>'
    end_tag = '</title>'
    start_index = rss_feed_str.find(start_tag)
    end_index = rss_feed_str.find(end_tag) + len(end_tag)
    title_tag = rss_feed_str[start_index:end_index]

    # Write only the title tag to the file
    with open('temperature_feed.xml', 'w') as f:
        f.write(title_tag)

# Generate RSS feed
generate_rss_feed()
