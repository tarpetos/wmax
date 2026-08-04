#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use rust_embed::RustEmbed;
use std::env;
use std::io::Cursor;
use tiny_http::{Header, Response, Server, StatusCode};

#[derive(RustEmbed)]
#[folder = "../src/"]
struct Asset;

fn main() {
    #[cfg(target_os = "linux")]
    if std::env::var_os("WEBKIT_DISABLE_DMABUF_RENDERER").is_none() {
        std::env::set_var("WEBKIT_DISABLE_DMABUF_RENDERER", "1");
        std::env::set_var("WEBKIT_DISABLE_COMPOSITING_MODE", "1");
    }

    let args: Vec<String> = env::args().collect();
    let mut host = String::from("127.0.0.1");
    let mut port = 8080;
    let mut server_mode = false;

    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--server" => {
                server_mode = true;
            }
            "--host" => {
                if i + 1 < args.len() {
                    host = args[i + 1].clone();
                    server_mode = true;
                    i += 1;
                }
            }
            "--port" => {
                if i + 1 < args.len() {
                    if let Ok(p) = args[i + 1].parse::<u16>() {
                        port = p;
                        server_mode = true;
                    }
                    i += 1;
                }
            }
            _ => {}
        }
        i += 1;
    }

    if server_mode {
        let addr = format!("{}:{}", host, port);
        println!("Starting WMAX server mode at http://{}", addr);
        let server = Server::http(&addr).unwrap();
        
        for request in server.incoming_requests() {
            let mut path = request.url().to_string();
            if path == "/" || path == "" {
                path = "index.html".to_string();
            } else if path.starts_with('/') {
                path = path[1..].to_string();
            }

            match Asset::get(&path) {
                Some(content) => {
                    let mime = mime_guess::from_path(&path).first_or_octet_stream();
                    let response = Response::from_data(content.data.into_owned())
                        .with_status_code(StatusCode(200))
                        .with_header(
                            Header::from_bytes(&b"Content-Type"[..], mime.as_ref().as_bytes())
                                .unwrap(),
                        );
                    let _ = request.respond(response);
                }
                None => {
                    let response = Response::from_string("404 Not Found")
                        .with_status_code(StatusCode(404));
                    let _ = request.respond(response);
                }
            }
        }
    } else {
        wmax_lib::run();
    }
}
