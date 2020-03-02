var ec_rank = echarts.init(document.getElementById("rank"), "dark");

var ec_rank_option = {
  title: {
    // 标题样式
    text: "非湖北地区城市确诊TOP10",
    textStyle: {
      color: "white"
    },
    left: "left"
  },
  color: ["#3398DB"],
  tooltip: {
    trigger: "axis",
    axisPointer: {
      // 坐标轴指示器，坐标轴触发有效
      type: "shadow" // 默认为直线，可选为：'line' | 'shadow'
    }
  },
  grid: {
    left: "3%",
    right: "4%",
    bottom: "3%",
    containLabel: true
  },
  xAxis: [
    {
      type: "category",
      data: [
        "重庆",
        "温州",
        "深圳",
        "北京",
        "广州",
        "郑州",
        "南阳",
        "信阳",
        "周口",
        "商丘"
      ]
    }
  ],
  yAxis: [
    {
      type: "value"
    }
  ],
  series: [
    {
      data: [10, 52, 200, 334, 390, 10, 52, 200, 334, 390],
      type: "bar",
      barWidth: "30%"
    }
  ]
};
ec_rank.setOption(ec_rank_option);
