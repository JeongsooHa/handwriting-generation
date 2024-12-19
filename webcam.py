#### text from webcam
from IPython.display import display, Javascript
from google.colab.output import eval_js
import cv2
import numpy as np
import PIL.Image
import base64

# 웹캠에서 이미지를 캡처하는 JavaScript 코드 실행
def capture_image():
    js = Javascript('''
    async function captureImage() {
      // 이전에 생성된 요소 제거
      const oldDiv = document.getElementById('webcam-container');
      if (oldDiv) {
        oldDiv.remove();
      }

      // 새 요소 생성
      const div = document.createElement('div');
      div.id = 'webcam-container';
      const video = document.createElement('video');
      const canvas = document.createElement('canvas');
      const button = document.createElement('button');
      const stopButton = document.createElement('button');

      // Video 설정
      video.style.display = 'block';
      button.textContent = 'Capture Image';
      stopButton.textContent = 'Stop Camera';

      div.appendChild(video);
      div.appendChild(button);
      div.appendChild(stopButton);
      document.body.appendChild(div);

      // 웹캠 스트림 가져오기
      const stream = await navigator.mediaDevices.getUserMedia({video: true});
      video.srcObject = stream;
      await video.play();

      // 버튼 이벤트 처리
      const imgPromise = new Promise((resolve) => {
        button.onclick = () => {
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
          canvas.getContext('2d').drawImage(video, 0, 0);
          stream.getTracks().forEach(track => track.stop());
          div.remove();
          resolve(canvas.toDataURL('image/png'));
        };
        stopButton.onclick = () => {
          stream.getTracks().forEach(track => track.stop());
          div.remove();
          resolve(null);
        };
      });
      return imgPromise;
    }
    captureImage();
    ''')
    display(js)
    data = eval_js('captureImage()')
    return data

# 이미지 처리
def save_webcam_image():
    print("웹캠을 열고 이미지를 캡처하세요!")
    data = capture_image()
    if data:
        # base64 데이터를 OpenCV 이미지로 변환
        img_data = data.split(",")[1]
        img_array = np.frombuffer(base64.b64decode(img_data), np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # 이미지 저장
        filename = "/content/sample_data/webcam_capture.png"
        cv2.imwrite(filename, img)
        print(f"이미지가 저장되었습니다: {filename}")

        # 저장된 이미지 출력
        display(PIL.Image.open(filename))
    else:
        print("캡처가 취소되었습니다.")

if __name__ == '__main__':
  save_webcam_image()
