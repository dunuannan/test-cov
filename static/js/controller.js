function get_time() {
  $.ajax({
    url: "/time",
    timeout: 10000,
    success: function(data) {
      $("#time").html(data);
    },
    error: function(xhr, type, errorThrown) {}
  });
}

function get_keyword() {
  $.ajax({
    url: "/keyword",
    time: 10000,
    success: function(data) {
      $(".num h1")
        .eq(0)
        .text(data.confirm);
      $(".num h1")
        .eq(1)
        .text(data.suspect);
      $(".num h1")
        .eq(2)
        .text(data.heal);
      $(".num h1")
        .eq(3)
        .text(data.dead);
    },
    error: function(xhr, type, errorThrown) {}
  });
}

function get_map_data() {
  $.ajax({
    url: "/map",
    time: 10000,
    success: function(data) {
      ec_map_option.series[0].data = data.data;
      ec_map.setOption(ec_map_option);
    },
    error: function(xhr, type, errorThrown) {}
  });
}

function get_total_data() {
  $.ajax({
    url: "/total",
    time: 10000,
    success: function(data) {
      ec_total_option.xAxis[0].data = data.day;
      ec_total_option.series[0].data = data.confirm;
      ec_total_option.series[1].data = data.suspect;
      ec_total_option.series[2].data = data.heal;
      ec_total_option.series[3].data = data.dead;
      ec_total.setOption(ec_total_option);
    },
    error: function(xhr, type, errorThrown) {}
  });
}

function get_add_data() {
  $.ajax({
    url: "/add",
    time: 10000,
    success: function(data) {
      ec_add_option.xAxis[0].data = data.day;
      ec_add_option.series[0].data = data.confirm_add;
      ec_add_option.series[1].data = data.suspect_add;
      ec_add.setOption(ec_add_option);
    },
    error: function(xhr, type, errorThrown) {}
  });
}

function get_rank_data() {
  $.ajax({
    url: "/rank",
    time: 10000,
    success: function(data) {
      ec_rank_option.xAxis[0].data = data.city;
      ec_rank_option.series[0].data = data.confirm;
      ec_rank.setOption(ec_rank_option);
    },
    error: function(xhr, type, errorThrown) {}
  });
}

function get_hot_data() {
  $.ajax({
    url: "/hot",
    time: 10000,
    success: function(data) {
      ec_hot_option.series[0].data = data.hotword;
      ec_hot.setOption(ec_hot_option);
    },
    error: function(xhr, type, errorThrown) {}
  });
}

setInterval(get_time, 1000);
// setInterval(get_keyword, 1000);
// setInterval(get_map_data, 1000);
// setInterval(get_total_data, 1000);
// setInterval(get_add_data, 1000);
// setInterval(get_rank_data, 1000);
// setInterval(get_hot_data, 1000);
get_total_data();
get_add_data();
get_keyword();
get_map_data();
get_rank_data();
get_hot_data();

