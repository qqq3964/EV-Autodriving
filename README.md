# EV Autodriving

</div>

## Part
- GPS (김현우)
- 영상처리 (김태완)
- 아두이노 하드웨어 컨트롤러 (송예원,정찬혁)
- LiDAR (박기영)

## 영상처리

sliding window 기법을 이용</br>
trouble shooting으로 비가 많이오는 날씨를 고려해 V-ROI을 채택하여 도로 가운데를 관심영역 밖으로 제외</br>
허프 필터를 사용하여 빛의 영역을 선으로 인식하였으나 날씨의 요소로 사용하지 못하였음</br>

### Flow Chart
1. bird eye view
2. V-ROI를 이용하여 라인이 있을만한 영역만 추출
3. 흰색 영역에 대해 hist그램을 이용해 영역추출
4. 추출한 히스토그램에서 슬라이딩 윈도우 기법을 적용
5. 각도로는 arctan를 이용하여 맵의 중심으로부터 얼마나 윈도우가 떨어졌는지 측정
6. 선이 하나만 보이는 상황에서는 한선으로 고려하도록 제한
### 시연 영상
![output (online-video-cutter com) (5)](https://github.com/qqq3964/EV-Autodriving/assets/97833069/9c4ddfcc-ded8-4060-aa86-d6f965d8d205)

## Team Members

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<table>
  <tr>
    <td align="center"><a href="https://github.com/qqq3964"><img src="https://avatars.githubusercontent.com/u/97833069?s=400&u=623611a57815c2322bb2947695dba0cf6a5c602e&v=4" width="100px;" alt=""/><br /><sub><b>Taewan Kim</b></sub></a><br /><a href="https://github.com/qqq3964" title="Code"></a></td>
    <td align="center"><a href="https://github.com/HarrysK99"><img src="https://avatars.githubusercontent.com/u/81846798?v=4" width="100px;" alt=""/><br /><sub><b>Hyunwoo Kim</b></sub></a><br /><a href="https://github.com/Kaintels" title="Code"></a></td>
    <td align="center"><a href="https://github.com/Wilbur-Babo"><img src="https://avatars.githubusercontent.com/u/61016569?v=4" width="100px;" alt=""/><br /><sub><b>Yewon Song</b></sub></a><br /><a href="https://github.com/Wilbur-Babo" title="Code"></a></td>
    <td align="center"><a href="https://github.com/stevekwon211"><img src="https://avatars.githubusercontent.com/u/61633137?s=400&u=fd514a668292884e640c15973976e0a0ec39fdbc&v=4" width="100px;" alt=""/><br /><sub><b>Chanhyeok Jung</b></sub></a><br /><a href="https://velog.io/@kwonhl0211" title="Code"></a></td>
    <td align="center"><a href="https://github.com/sw-song"><img src="https://avatars.githubusercontent.com/u/116241982?v=4" width="100px;" alt=""/><br /><sub><b>Kiyoung Park</b></sub></a><br /><a href="https://www.linkedin.com/in/seungwonsong/" title="Code"></a></td>
  </tr>
</table>
