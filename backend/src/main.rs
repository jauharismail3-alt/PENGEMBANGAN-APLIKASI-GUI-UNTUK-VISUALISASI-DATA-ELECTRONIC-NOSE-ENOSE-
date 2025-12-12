use serde::{Deserialize, Serialize};
use std::sync::{Arc, Mutex};
use std::time::{SystemTime, UNIX_EPOCH};
use std::io::{self, Read};
use std::net::TcpListener;
use std::thread;
use std::time::Duration;
use actix_web::{get, web, App, HttpServer, HttpResponse, Responder};
use reqwest::Client;
use tokio::runtime::Runtime;

// ==================== STRUCTURES (TIDAK BERUBAH) ====================
#[derive(Serialize, Deserialize, Clone, Debug)]
struct SensorPacket {
    timestamp: u64,
    sample: String,
    no2: f64,
    eth_gm: f64, 
    voc_gm: f64,
    co_gm: f64,
    co_m: f64,
    eth_m: f64,
    voc_m: f64,
    current_state: i32,
    current_level: i32,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
struct InfluxConfig {
    url: String,
    token: String,
    org: String,
    bucket: String,
}

// ==================== APP STATE (DITAMBAH INFLUX CONFIG) ====================
#[derive(Clone)]
struct AppState {
    buffer: Arc<Mutex<Vec<SensorPacket>>>,
    arduino_connected: Arc<Mutex<bool>>,
    current_level: Arc<Mutex<i32>>,
    current_state: Arc<Mutex<i32>>,
    influx_config: Arc<Mutex<InfluxConfig>>,  // ✅ BARU
}

impl AppState {
    fn new() -> Self {
        AppState {
            buffer: Arc::new(Mutex::new(Vec::new())),
            arduino_connected: Arc::new(Mutex::new(false)),
            current_level: Arc::new(Mutex::new(0)),
            current_state: Arc::new(Mutex::new(0)),
            influx_config: Arc::new(Mutex::new(InfluxConfig {
                url: "http://localhost:8086".to_string(),
                token: "sdTbrLbJ_ercWHAoZ0-rdQJtLvm-Bc13o7xyN_YPWgsmh3_4-v1-hgrh2MwnZePeO3PEZrl7uxxpRPdI72hdrQ==".to_string(),
                org: "sps".to_string(),
                bucket: "enose_data".to_string(),
            })),
        }
    }
}

fn parse_arduino_data(line: &str) -> Option<SensorPacket> {
    let cleaned_line = line.trim();
    println!("📨 Raw Arduino data: {}", cleaned_line);
    
    // ✅ FORMAT 1: JSON (kelompok lain)
    if cleaned_line.starts_with('{') {
        if let Ok(parsed) = serde_json::from_str::<serde_json::Value>(cleaned_line) {
            println!("🔍 Parsing JSON format");
            
            // Extract values dari JSON
            let no2 = parsed["no2_gm"].as_f64().unwrap_or(-1.0);
            let eth_gm = parsed["c2h5oh_gm"].as_f64().unwrap_or(-1.0);
            let voc_gm = parsed["voc_gm"].as_f64().unwrap_or(-1.0);
            let co_gm = parsed["co_gm"].as_f64().unwrap_or(-1.0);
            let co_m = parsed["co_mics"].as_f64().unwrap_or(-1.0);
            let eth_m = parsed["eth_mics"].as_f64().unwrap_or(-1.0);
            let voc_m = parsed["voc_mics"].as_f64().unwrap_or(-1.0);
            
            // Parse state dari string ke integer
            let state_str = parsed["state"].as_str().unwrap_or("IDLE");
            let current_state = match state_str {
                "IDLE" => 0,
                "PRE_COND" => 1,
                "RAMP_UP" => 2,
                "HOLD" => 3,
                "PURGE" => 4,
                "RECOVERY" => 5,
                "DONE" => 6,
                _ => 0
            };
            
            let current_level = parsed["currentLevel"].as_i64().unwrap_or(0) as i32;
            
            let packet = SensorPacket {
                timestamp: SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_millis() as u64,
                sample: "Active".to_string(),
                no2,
                eth_gm,
                voc_gm,
                co_gm,
                co_m,
                eth_m,
                voc_m,
                current_state,
                current_level,
            };
            
            println!("✅ Successfully parsed JSON data");
            return Some(packet);
        } else {
            println!("❌ Failed to parse JSON");
        }
    }
    
    // ✅ FORMAT 2: SENSOR: CSV (format original Anda)
    if cleaned_line.starts_with("SENSOR:") {
        let data_part = &cleaned_line[7..];
        let parts: Vec<&str> = data_part.split(',').collect();
        
        println!("🔍 Parsed {} parts: {:?}", parts.len(), parts);
        
        if parts.len() == 9 {
            let no2 = parts[0].parse().unwrap_or(-1.0);
            let eth_gm = parts[1].parse().unwrap_or(-1.0);
            let voc_gm = parts[2].parse().unwrap_or(-1.0);
            let co_gm = parts[3].parse().unwrap_or(-1.0);
            let co_m = parts[4].parse().unwrap_or(-1.0);
            let eth_m = parts[5].parse().unwrap_or(-1.0);
            let voc_m = parts[6].parse().unwrap_or(-1.0);
            let current_state = parts[7].parse().unwrap_or(0);
            let current_level = parts[8].parse().unwrap_or(0);
            
            let packet = SensorPacket {
                timestamp: SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_millis() as u64,
                sample: "Active".to_string(),
                no2,
                eth_gm,
                voc_gm,
                co_gm,
                co_m,
                eth_m,
                voc_m,
                current_state,
                current_level,
            };
            
            println!("✅ Successfully parsed SENSOR: format");
            return Some(packet);
        }
    }
    
    // ✅ FORMAT 3: Direct CSV tanpa prefix
    let parts: Vec<&str> = cleaned_line.split(',').collect();
    if parts.len() == 9 {
        let no2 = parts[0].parse().unwrap_or(-1.0);
        let eth_gm = parts[1].parse().unwrap_or(-1.0);
        let voc_gm = parts[2].parse().unwrap_or(-1.0);
        let co_gm = parts[3].parse().unwrap_or(-1.0);
        let co_m = parts[4].parse().unwrap_or(-1.0);
        let eth_m = parts[5].parse().unwrap_or(-1.0);
        let voc_m = parts[6].parse().unwrap_or(-1.0);
        let current_state = parts[7].parse().unwrap_or(0);
        let current_level = parts[8].parse().unwrap_or(0);
        
        let packet = SensorPacket {
            timestamp: SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_millis() as u64,
            sample: "Active".to_string(),
            no2,
            eth_gm,
            voc_gm,
            co_gm,
            co_m,
            eth_m,
            voc_m,
            current_state,
            current_level,
        };
        
        println!("✅ Successfully parsed DIRECT format");
        return Some(packet);
    }
    
    println!("❌ Cannot parse data: unexpected format - '{}'", cleaned_line);
    None
}

fn send_to_influxdb(data: &SensorPacket, config: &InfluxConfig) {
    let rt = Runtime::new().unwrap();
    
    rt.block_on(async {
        let client = Client::new();
        let url = format!("{}/api/v2/write?org={}&bucket={}&precision=ns", 
            config.url, config.org, config.bucket);
        
        let line_protocol = format!(
            "sensor_data,sensor_type=enose,state={},level={} no2={},eth_gm={},voc_gm={},co_gm={},co_m={},eth_m={},voc_m={} {}",
            data.current_state,
            data.current_level,
            data.no2, data.eth_gm, data.voc_gm, data.co_gm, data.co_m, data.eth_m, data.voc_m,
            data.timestamp * 1_000_000
        );
        
        // ✅ DEBUG: Print URL dan data
        println!("🔧 InfluxDB Debug:");
        println!("   URL: {}", url);
        println!("   Data: {}", line_protocol);
        
        match client
            .post(&url)
            .header("Authorization", format!("Token {}", config.token))
            .header("Content-Type", "text/plain")
            .body(line_protocol)
            .send()
            .await {
                Ok(response) => {
                    println!("   Status: {}", response.status());
                    if response.status().is_success() {
                        println!("✅ Data sent to InfluxDB successfully");
                    } else {
                        // ✅ DEBUG: Print error response
                        let error_body = response.text().await.unwrap_or_default();
                        println!("❌ InfluxDB error: {}", error_body);
                    }
                }
                Err(e) => {
                    println!("❌ Failed to send to InfluxDB: {}", e);
                }
            }
    });
}

// ==================== TCP SERVER (DITAMBAH INFLUXDB) ====================
fn tcp_server_worker(state: AppState) {
    println!("🔌 Starting TCP server on 0.0.0.0:8081");
    
    match TcpListener::bind("0.0.0.0:8081") {
        Ok(listener) => {
            println!("✅ TCP Server started on 0.0.0.0:8081");
            
            listener.set_nonblocking(true).expect("Cannot set non-blocking");
            
            let mut connection_count = 0;
            
            loop {
                match listener.accept() {
                    Ok((stream, addr)) => {
                        connection_count += 1;
                        println!("✅ Arduino connected from: {} (Connection #{})", addr, connection_count);
                        
                        let state_for_thread = state.clone();
                        thread::spawn(move || {
                            handle_arduino_connection(stream, state_for_thread);
                        });
                    }
                    Err(e) => {
                        if e.kind() == io::ErrorKind::WouldBlock {
                            thread::sleep(Duration::from_millis(50));
                            continue;
                        } else {
                            eprintln!("❌ TCP accept error: {}", e);
                        }
                    }
                }
            }
        }
        Err(e) => {
            eprintln!("❌ Failed to start TCP server: {}", e);
        }
    }
}

// ==================== HANDLE ARDUINO CONNECTION (DITAMBAH INFLUXDB) ====================
fn handle_arduino_connection(mut stream: std::net::TcpStream, state: AppState) {
    println!("🔌 Handling Arduino connection...");
        
    stream.set_nonblocking(true).ok();
    stream.set_read_timeout(Some(Duration::from_secs(1))).ok();
    
    let mut buffer_data = [0; 1024];
    let mut connection_active = true;
    
    while connection_active {
        match stream.read(&mut buffer_data) {
            Ok(0) => {
                println!("🔌 Arduino disconnected (graceful)");
                connection_active = false;
            }
            Ok(size) => {
                let received_data = String::from_utf8_lossy(&buffer_data[..size]);
                let lines: Vec<&str> = received_data.split('\n').collect();
                
                println!("📨 Received {} bytes, {} lines", size, lines.len());
                
                for line in lines {
                    let trimmed_line = line.trim();
                    if !trimmed_line.is_empty() {
                        println!("📝 Processing: {}", trimmed_line);
                        
                        if let Some(sensor_data) = parse_arduino_data(trimmed_line) {
                            // Update state (TIDAK BERUBAH)
                            {
                                let mut level = state.current_level.lock().unwrap();
                                *level = sensor_data.current_level;
                                
                                let mut state_val = state.current_state.lock().unwrap();
                                *state_val = sensor_data.current_state;
                                
                                let mut connected = state.arduino_connected.lock().unwrap();
                                *connected = true;
                            }
                            
                            // Store in buffer (TIDAK BERUBAH)
                            {
                                let mut buf = state.buffer.lock().unwrap();
                                buf.push(sensor_data.clone());
                                
                                if buf.len() > 1000 {
                                    buf.remove(0);
                                }
                                
                                println!("💾 Stored data point. Total: {}", buf.len());
                            }
                            
                            // ✅ BARU: Kirim ke InfluxDB
                            let config = state.influx_config.lock().unwrap();
                            send_to_influxdb(&sensor_data, &config);
                            
                            // Print received data
                            println!("📊 Sensor Data - NO2: {:.2}, Ethanol: {:.2}, VOC: {:.2}, State: {}, Level: {}",
                                sensor_data.no2, sensor_data.eth_gm, sensor_data.voc_gm,
                                sensor_data.current_state, sensor_data.current_level);
                        }
                    }
                }
                
                buffer_data = [0; 1024];
                connection_active = false;
            }
            Err(e) => {
                if e.kind() == io::ErrorKind::WouldBlock {
                    connection_active = false;
                } else if e.kind() == io::ErrorKind::TimedOut {
                    connection_active = false;
                } else {
                    eprintln!("❌ TCP read error: {}", e);
                    connection_active = false;
                }
            }
        }
    }
    
    println!("🔌 Arduino connection handler finished");
}

// ==================== HTTP ENDPOINTS UNTUK PYQT6 (BARU) ====================
#[get("/api/status")]
async fn get_status(data: web::Data<AppState>) -> impl Responder {
    let connected = data.arduino_connected.lock().unwrap();
    let level = data.current_level.lock().unwrap();
    let current_state = data.current_state.lock().unwrap();
    let buffer = data.buffer.lock().unwrap();
    
    HttpResponse::Ok().json(serde_json::json!({
        "arduino_connected": *connected,
        "current_level": *level,
        "current_state": *current_state,
        "data_points": buffer.len()
    }))
}

#[get("/api/data")]
async fn get_data(data: web::Data<AppState>) -> impl Responder {
    let buffer = data.buffer.lock().unwrap();
    HttpResponse::Ok().json(&*buffer)
}

#[get("/api/csv")]
async fn get_csv(data: web::Data<AppState>) -> impl Responder {
    let buffer = data.buffer.lock().unwrap();
    
    if buffer.is_empty() {
        return HttpResponse::NoContent().body("No data available");
    }
    
    let mut csv_output = String::new();
    
    // ✅ HEADER 100% Edge Impulse Compatible
    csv_output.push_str("timestamp,GMXXX_NO2 (ppm),GMXXX_Ethanol (ppm),GMXXX_VOC (ppm),GMXXX_CO (ppm),MiCS5524_CO (ppm),MiCS5524_Ethanol (ppm),MiCS5524_VOC (ppm),label\n");
    
    // Data rows - format perfect untuk Edge Impulse
    for packet in buffer.iter() {
        // Generate meaningful labels berdasarkan state dan level
        let label = if packet.current_level > 0 {
            format!("level_{}_state_{}", packet.current_level, packet.current_state)
        } else {
            "idle".to_string()
        };
        
        csv_output.push_str(&format!(
            "{},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{}\n",
            packet.timestamp,     // milliseconds timestamp
            packet.no2.max(0.0),          // GMXXX_NO2 - pastikan tidak negatif
            packet.eth_gm.max(0.0),       // GMXXX_Ethanol  
            packet.voc_gm.max(0.0),       // GMXXX_VOC
            packet.co_gm.max(0.0),        // GMXXX_CO
            packet.co_m.max(0.0),         // MiCS5524_CO
            packet.eth_m.max(0.0),        // MiCS5524_Ethanol
            packet.voc_m.max(0.0),        // MiCS5524_VOC
            label                        // Label untuk classification
        ));
    }
    
    HttpResponse::Ok()
        .content_type("text/csv")
        .header("Content-Disposition", "attachment; filename=enose_data_edge_impulse.csv")
        .body(csv_output)
}

#[get("/api/csv/timeseries")]
async fn get_csv_timeseries(data: web::Data<AppState>) -> impl Responder {
    let buffer = data.buffer.lock().unwrap();
    
    if buffer.is_empty() {
        return HttpResponse::NoContent().body("No data available");
    }
    
    let mut csv_output = String::new();
    
    // ✅ HEADER untuk Time-series Classification
    csv_output.push_str("timestamp,GMXXX_NO2,GMXXX_Ethanol,GMXXX_VOC,GMXXX_CO,MiCS5524_CO,MiCS5524_Ethanol,MiCS5524_VOC,state,level,label\n");
    
    // Data rows dengan metadata lengkap
    for packet in buffer.iter() {
        let state_name = match packet.current_state {
            0 => "idle",
            1 => "pre_conditioning", 
            2 => "ramp_up",
            3 => "hold",
            4 => "purge",
            5 => "recovery", 
            6 => "done",
            _ => "unknown"
        };
        
        let label = if packet.current_level > 0 {
            format!("sampling_level_{}", packet.current_level)
        } else {
            "idle".to_string()
        };
        
        csv_output.push_str(&format!(
            "{},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{},{},{}\n",
            packet.timestamp,
            packet.no2.max(0.0),
            packet.eth_gm.max(0.0),  
            packet.voc_gm.max(0.0),
            packet.co_gm.max(0.0),
            packet.co_m.max(0.0),
            packet.eth_m.max(0.0),
            packet.voc_m.max(0.0),
            state_name,              // State sebagai string
            packet.current_level,    // Level sebagai number
            label                   // Label untuk classification
        ));
    }
    
    HttpResponse::Ok()
        .content_type("text/csv")
        .header("Content-Disposition", "attachment; filename=enose_timeseries_edge_impulse.csv")
        .body(csv_output)
}

#[get("/api/config/influx")]
async fn get_influx_config(data: web::Data<AppState>) -> impl Responder {
    let config = data.influx_config.lock().unwrap();
    HttpResponse::Ok().json(&*config)
}

// ==================== MAIN (DITAMBAH HTTP SERVER) ====================
#[actix_web::main]
async fn main() -> std::io::Result<()> {
    println!("🚀 Electronic Nose Backend - Multi Service");
    println!("🔌 TCP Server on port 8081 (Arduino)");
    println!("🌐 HTTP API on port 8080 (PyQt6 Frontend)");
    println!("📊 InfluxDB integration ready");
    println!("🎯 Waiting for connections...");
    
    let state = AppState::new();
    
    // THREAD 1: TCP Server untuk Arduino (Port 8081)
    let state_tcp = state.clone();
    thread::spawn(move || {
        tcp_server_worker(state_tcp);
    });
    
    // THREAD 2: HTTP Server untuk PyQt6 (Port 8080) - PORT BERBEDA!
    println!("🌐 Starting HTTP Server on port 8080...");
    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(state.clone()))
            .service(get_status)
            .service(get_data)
            .service(get_influx_config)
            .service(get_csv)
    })
    .bind(("0.0.0.0", 8080))?  // ✅ PORT BERBEDA!
    .run()
    .await
}

