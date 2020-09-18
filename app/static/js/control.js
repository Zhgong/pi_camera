class MyController {
    constructor(doms, camera) {
      this.doms = doms;
      this.camera = camera
      this.value = 5;
      this.btnStartRecording = this.doms.btnStartRecording;
      console.log(this.value);
    }
    init() {
      this.addEventStartRecording();
    }

    addEventStartRecording() {
      const that = this;
      this.btn.addEventListener("click", e => {
        console.log("start clicked");
        // await that.camera.startRecording();
        // console.log(result);
      });
    }
  }
