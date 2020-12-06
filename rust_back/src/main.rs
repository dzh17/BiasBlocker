
#[macro_use]
extern crate lazy_static;
extern crate actix_cors;
extern crate reqwest;
extern crate futures;

use actix_web::{post, get, web, App, HttpServer, Responder};
use actix_web::web::Path;
use serde_json::{ Value };
use std::collections::HashMap;
use serde::{ Deserialize, Serialize };
use std::fs;
use chrono::prelude::*;
use actix_cors::{Cors, CorsFactory};
use actix_web::http::{header};
use futures::future;
use std::env;

#[derive(Serialize, Deserialize, Debug)]
pub struct RelatedArticle {
    score: f32,
    link: String,
    title: String,
    pubDate: String,
    content: String,
    image: String
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Article {
    link: String,
    title: String,
    pubDate: String,
    content: String,
    images: Vec<String>,
    keywords: Vec<Keyword>
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Keyword {
    label: String,
    label_weight: f32,
    occurencies: i32,
    synonyms: Vec<String>,
    value: String,
    weight: f32,
    words_count: i32
}

#[derive(Serialize, Deserialize, Debug)]
pub struct InputArticle {
    title: String,
    content: String,
    keywords: Vec<Keyword>
}


lazy_static! {
    static ref HASHMAP: HashMap<u32, &'static str> = {
        let mut m = HashMap::new();
        m.insert(0, "foo");
        m.insert(1, "bar");
        m.insert(2, "baz");
        m
    };
    static ref AZ_ARTICLES: Vec<Article> = {
        println!("Reading az -> static");
        let file = fs::File::open("az_weight.json").expect("File should open read only");
        let articles: Vec<Article> = serde_json::from_reader(file).unwrap();
        println!("Finished am -> reading");
        articles

    };
    static ref AM_ARTICLES: Vec<Article> = {
        println!("Reading am -> static");
        let file = fs::File::open("am_weight.json").expect("File should open read only");
        let articles: Vec<Article> = serde_json::from_reader(file).unwrap();
        println!("Finished am -> reading");
        articles
    };
}

#[get("/say_hello")]
async fn say_hello() -> impl Responder {
    return "Working totally fine"
}

#[post("/related_articles/{country}")]
async fn echo(req_body: String, params: Path<(String)>) -> impl Responder {
    let country = params.to_lowercase();
    let parsed_json: Value = serde_json::from_str(req_body.as_str()).unwrap();
    let article_title: String = parsed_json["article_title"].to_string();
    let article_text: String = parsed_json["article_text"].to_string();
    let article_date: String = parsed_json["article_date"].to_string();

    let mut map = HashMap::new();
    map.insert("article_date", article_date.clone());
    map.insert("article_title", article_title.clone());
    map.insert("article_text", article_text.clone());

    let client = reqwest::Client::new();
    
    let response = client.post("https://pyparser.herokuapp.com/parse_article/j/")
        .json(&map)
        .send()
        .await
        .unwrap()
        .text()
        .await
        .unwrap();
    let cleaned_text = response.clone().to_string().replace("\\\"", "");
    let input_article: InputArticle = serde_json::from_str(cleaned_text.as_str()).unwrap();
    let mut related_articles: Vec<RelatedArticle> = vec![];
    let my_date = article_date.clone().to_string().replace("\"", "");
    let input_article_pub_date = NaiveDateTime::parse_from_str(&my_date, "%Y-%m-%dT%H:%M:%S").unwrap();
    if country == "am" {
        for i in 0..AM_ARTICLES.len() {
            let article = AM_ARTICLES.get(i).unwrap();
            let date: String = article.pubDate.replace("\"", "").chars().take(19).collect();
            println!("Pub date : {:?}", date);
            if let Ok(article_pub_date) = NaiveDateTime::parse_from_str(date.as_str(), "%Y-%m-%dT%H:%M:%S") {
                if article_pub_date.signed_duration_since(input_article_pub_date).num_days().abs() <= 2 {
                    let total_score = compare_articles(&input_article, &article);
                    println!("{:?} {:?}", article.title, total_score);
                    let mut the_image: String = "".to_string();
                    if let Some(image) = article.images.get(0) {
                        the_image = image.to_string();
                    }
                    related_articles.push(RelatedArticle { 
                        score: total_score, 
                        title: article.title.clone(),
                        link: article.link.clone(),
                        pubDate: article.pubDate.clone(),
                        content: article.content.clone(),
                        image: the_image.clone()
                    });
                }
            }            
        }
    } else {
        for i in 0..AZ_ARTICLES.len() {
            let article = AZ_ARTICLES.get(i).unwrap();
            let date: String = article.pubDate.replace("\"", "").chars().take(19).collect();
            println!("Pub date : {:?}", date);
            if let Ok(article_pub_date) = NaiveDateTime::parse_from_str(date.as_str(), "%Y-%m-%dT%H:%M:%S") {
                if article_pub_date.signed_duration_since(input_article_pub_date).num_days().abs() <= 2 {
                    let total_score = compare_articles(&input_article, &article);
                    println!("{:?} {:?}", article.title, total_score);
                    let mut the_image: String = "".to_string();
                    if let Some(image) = article.images.get(0) {
                        the_image = image.to_string();
                    }
                    related_articles.push(RelatedArticle { 
                        score: total_score, 
                        title: article.title.clone(),
                        link: article.link.clone(),
                        pubDate: article.pubDate.clone(),
                        content: article.content.clone(),
                        image: the_image.clone()
                    });
                }
            }   
        }
    }
   
    related_articles.sort_by(|a, b| b.score.partial_cmp(&a.score).unwrap());
    let first_articles: Vec<RelatedArticle> = related_articles.into_iter().take(5).collect::<Vec<RelatedArticle>>();
    web::Json(first_articles)
}

fn compare_articles(article_1 :&InputArticle, article_2 :&Article) -> f32 {
    let mut total_score = 0.0;
    for i in 0..article_1.keywords.len() {
        let keyword_1 = article_1.keywords.get(i).unwrap();
        let keyword_1_label = &keyword_1.label;
        let keyword_1_value = &keyword_1.value;
        let keyword_1_weight = &keyword_1.weight;

        for j in 0..article_2.keywords.len() {
            let keyword_2 = &article_2.keywords.get(j).unwrap();
            let keyword_2_label = &keyword_2.label;
            let keyword_2_value = &keyword_2.value;
            let keyword_2_weight = &keyword_2.weight;
            let keyword_2_synonyms = &keyword_2.synonyms;
            let mut local_comparison_score = 0.0;
            if (keyword_1_label == "NOUN" || keyword_1_label == "VERB" || keyword_1_label == "DATE") &&
               (keyword_2_label == "NOUN" || keyword_2_label == "VERB" || keyword_2_label == "DATE")  {
                if  keyword_2_synonyms.contains(&keyword_1_value) {
                    local_comparison_score = keyword_1_weight * keyword_2_weight;
                } else {
                    local_comparison_score = 0.0;
                }
            } else {
                if keyword_2_label != "NOUN" && keyword_2_label != "VERB" && keyword_2_label != "DATE" {
                    if keyword_1_value.to_lowercase().contains(&keyword_2_value.to_lowercase()) || 
                    keyword_2_value.to_lowercase().contains(&keyword_1_value.to_lowercase()) {
                        local_comparison_score = keyword_1_weight * keyword_2_weight;
                    } else {
                        local_comparison_score = 0.0;
                    }
                }
            }
            total_score = total_score + local_comparison_score;
        }
    }
    total_score
}

#[actix_rt::main]
async fn main() -> std::io::Result<()> { 
    println!("Started loading...");
    
    let future_one = async {
        println!("{}", "He");
        println!("{:#?}", AM_ARTICLES.get(0));
        println!("{:#?}", AZ_ARTICLES.get(0));
    };

    let port = get_port();
    let server = HttpServer::new(move || {
        App::new()
            .wrap(get_cors())            
            .service(echo)
            .service(say_hello)
    })
    .bind(format!("{}:{}", "0.0.0.0", port))?
    .run();

    // Run both futures to completion, printing "foo" twice:
    future::join(server, future_one).await;
    Ok(())
}
    
fn get_cors() -> CorsFactory {
    Cors::new()
        .allowed_methods(vec!["GET", "POST", "PUT", "DELETE"])
        .allowed_headers(vec![header::AUTHORIZATION, header::ACCEPT])
        .allowed_header(header::CONTENT_TYPE)
        .max_age(3600)
        .finish()  
}  

fn get_port() -> String {
    let port: String = env::var("PORT").unwrap_or_else(|_| "3000".to_string()).parse().expect("PORT must be a number");
    return port;
}
