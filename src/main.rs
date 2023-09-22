use regex::Regex;

struct PodcastLink {
    itunes_id : i32,
    link : String
}

fn main () {
    // Pattern for matching podcast genres 
    let re_genre = Regex::new(r"https:\/\/podcasts\.apple\.com\/us\/genre\/podcasts-(\w+)(-\w+)+\/id(\d+)").unwrap();
    // Pattern for matching unique podcast URIs
    let re_podcast = Regex::new(r"https://podcasts.apple.com/us/podcast/((\w)+|(\w)+-(\w)+)/id(\d)+")
        .unwrap();

    // Container for podcast links
    let mut podcast_uris : Vec<_> = Vec::new();

    // HTTP Request to Itunes Podcast Website
    let resp = reqwest::blocking::get("https://podcasts.apple.com/us/genre/podcasts/id26");

    // HTML Content of concluded HTTP Request
    let html_content = resp.unwrap().text().unwrap();

    // Look for matches in the HTML content of the page
    let matches : Vec<_> = re_genre.find_iter(html_content.as_ref())
        .map(|m| m.as_str())
        .collect();
   
    // For each genre page, get a podcast link and add it uniquely to collection
    for link in matches {
        let resp = reqwest::blocking::get(link);
        
        let html_content = resp.unwrap().text().unwrap();
        
        let mut link_matches : Vec<_> = re_podcast.find_iter(html_content.as_ref())
            .map(|m| m.as_str().to_string())
            .collect();
    
        podcast_uris.append(&mut link_matches); 
    }

    
}

