var ec_map = echarts.init(document.getElementById("map"), "dark");
var mydata = [
  { name: "上海", value: 318 },
  { name: "云南", value: 162 }
];

var ec_map_option = {
  title: {
    text: "",
    subtext: "",
    x: "left"
  },
  tooltip: {
    trigger: "item"
  },
  //左侧小导航图标
  visualMap: {
    show: true,
    x: "left",
    y: "bottom",
    textStyle: {
      fontSize: 8,
      color: "white"
    },
    splitList: [
      { start: 1, end: 9 },
      { start: 10, end: 99 },
      { start: 100, end: 999 },
      { start: 1000, end: 9999 },
      { start: 10000 }
    ],
    color: ["#8A3310", "#C64918", "#E55B25", "#F2AD92", "#F9DCD1"]
  },
  //配置属性
  series: [
    {
      name: "累计确诊人数",
      type: "map",
      mapType: "china",
      roam: false,
      itemStyle: {
        normal: {
          borderWidth: 0.5, //区域边框宽度
          borderColor: "#009FE8", //区域边框颜色
          areaColor: "#FFEFD5" //区域颜色
        },
        emphasis: {
          //鼠标滑过地图高亮的相关设置
          borderWidth: 0.5,
          borderColor: "#4B0082",
          areaColor: "#FFFFFF"
        }
      },
      label: {
        normal: {
          show: true, //省份名称
          fontSize: 8
        },
        emphasis: {
          show: true, //省份名称
          fontSize: 8
        }
      },
      data: mydata //数据
    }
  ]
};
ec_map.setOption(ec_map_option);
