CREATE TABLE podcasts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    itunes_id VARCHAR(255),
    rss_link TEXT
);

CREATE TABLE episodes (
    id SERIAL PRIMARY KEY,
    podcast_id INTEGER REFERENCES podcasts(id),  -- Foreign Key
    title VARCHAR(255) NOT NULL,
    mp3_url TEXT,
    transcript TEXT
);
