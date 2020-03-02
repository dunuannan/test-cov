var ec_add = echarts.init(document.getElementById("add"), "dark");

var ec_add_option = {
  title: {
    // 标题样式
    text: "全国新增趋势",
    textStyle: {
      color: "white"
    },
    left: "left"
  },
  tooltip: {
    trigger: "axis",
    // 指示器
    axisPointer: {
      type: "line",
      lineStyle: {
        color: "#7171C6"
      }
    }
  },
  legend: {
    data: ["新增确诊", "新增疑似"],
    left: "right"
  },
  // 图形位置
  grid: {
    left: "4%",
    right: "6%",
    bottom: "4%",
    top: 50,
    containLabel: true
  },
  toolbox: {
    feature: {
      saveAsImage: {
        show: false
      },
    //   magicType: { type: ["line", "bar"] }
    }
  },
  xAxis: [
    {
      type: "category",
      // x轴坐标点开始与结束点位置都不在最边缘
      // boundaryGap: false,
      data: ["01.20", "01.21", "01.22"]
    }
  ],
  yAxis: [
    {
      type: "value",
      // y轴字体设置
      axisLable: {
        show: true,
        color: "white",
        fontSize: 12,
        formatter: function(value) {
          if (value >= 1000) {
            value = value / 1000 + "k";
          }
          return value;
        }
      },
      // y轴线设置显示
      axisLine: {
        show: true
      },
      // 与x轴平行的线样式
      splitLine: {
        show: true,
        lineStyle: {
          color: "#17273B",
          width: 1,
          type: "solid"
        }
      }
    }
  ],
  series: [
    {
      name: "新增确诊",
      type: "line",
      smooth: true,
      data: [260, 406, 600]
    },
    {
      name: "新增疑似",
      type: "line",
      smooth: true,
      data: [54, 37, 3935]
    }
  ]
};
ec_add.setOption(ec_add_option);
