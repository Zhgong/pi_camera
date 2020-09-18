class Camera{
    constructor(){
        
    }
    
  async startRecording() {
    const url = "http://127.0.0.1:5000/api/v1/record";
    const response = await fetch(url);
    const data = await response.json();
    return data;
  }
}