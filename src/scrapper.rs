use hyper::Client;

enum PodcastSource {
    Itunes,
    Spotify,
    PodcastIndexOrg
}

struct Scrapper {
    podcastSource : PodcastSource,

}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let client = Client::new();
    
    let uri = "


    Ok(())
}


