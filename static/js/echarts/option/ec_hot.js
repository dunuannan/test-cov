var ec_hot = echarts.init(document.getElementById("hot"), "dark");

var mydata = [
  { name: "肺炎", value: "127346700" },
  { name: "实时", value: "12734670" },
  { name: "新型", value: "12734670" }
];

var ec_hot_option = {
  title: {
    text: "今日疫情热搜",
    textStyle: {
      color: "white"
    },
    left: "left"
  },
  tooltip: {
    show: false
  },
  series: [
    {
      type: "wordCloud",
      gridSize: 1,
      sizeRange: [12, 55],
      rotationRange: [-45, 0, 45, 90],
      textStyle: {
        normal: {
          color: function() {
            return (
              "rgb(" +
              [
                Math.round(Math.random() * 255),
                Math.round(Math.random() * 255),
                Math.round(Math.random() * 255)
              ].join(",") +
              ")"
            );
          }
        },
        right: null,
        bottom: null
      },
      data: mydata
    }
  ]
};

ec_hot.setOption(ec_hot_option);
