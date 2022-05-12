//
// var dataset = [15,  20, 30, 40, 50, 100, 200]
// var width = 600
// var height = 600
//
// var svg = d3.select("body")
//             .append("svg")
//             .attr("width", width + 400)
//             .attr("height", height + 400)
//             .append('g')
//             .attr('transform', 'translate(10, 0)');
//
// var widthScale = d3.scaleLinear().domain([0, 400]).range([0, width])
// var colorScale = d3.scaleLinear().domain([0, 400]).range(['red', 'blue'])
// var axis       = d3.axisBottom().scale(widthScale)
// // var circle =  svg.append('circle')
// //     .attr('cx', 250)
// //     .attr('cy', 250)
// //     .attr('r', 50)
// //     .attr('fill', 'red');
// //
// // var rect = svg.append('rect')
// //               .attr('width', 100)
// //               .attr('height', 50);
// //
// // var line = svg.append('line')
// //               .attr('x1', 0)
// //               .attr('y1', 200)
// //               .attr('x2', 400)
// //               .attr('y2', 400)
// //               .attr('stroke', 'green')
// //               .attr('stroke-width', 10);
//
//
//
//
// var bars = svg.selectAll("rect")
//               .data(dataset)
//               .enter()
//                 .append('rect')
//                 .attr('width', function (value, i) {
//                   return widthScale(value);
//                 })
//                 .attr('height', "2vh")
//                 .attr('y', function(value, i) {
//                   return i* 50
//                 })
//                 .attr('fill', function (value, i){
//                   return colorScale(value * 30)
//                 })
//
// svg.append('g')
//   .attr('transform', 'translate(0, 350)')
//   .call(axis)
//
//
// bars.transition()
//     .delay(2000)
//     .duration(1000)
//     .attr('height', '1.2vh')
//     .transition()
//     .delay(200)
//     .duration(500)
//     .attr('fill', function (value){
//       return colorScale(value)
//     })
//
// var circles = svg.append('g')
//                 .attr('transform', 'translate(100, 500)')
//                 .selectAll('circle')
//                 .data(dataset)
//                 .enter()
//                   .append('circle')
//                   .attr('cx', function (value) {
//                     return Math.random() * 300
//                   })
//                   .attr('cy', function (value){
//                     return Math.random() * 300
//                   })
//                   .attr('r', function (value){
//                     return Math.random() * 100
//                   })
//                   .attr('fill', function(value) {
//                     return colorScale(value)
//                   })
//                   .attr('opacity', '0.5')
//
// // var circles = svg.append('circle')
// //                 .attr('transform', 'translate(100, 500)')
// //                 .attr('fill', 'blue')
// //                 .attr('cx', 400)
// //                 .attr('cy', 400)
// //                 .attr('r', 50)
//
//
// circles.transition()
//   .delay(2000)
//   .duration(1500)
//   .attr('cx', function(value){
//     return Math.random() * 400
//   })
//   .attr('cy', function(value){
//     return Math.random() * 400
//   })
//   .attr('fill', function(value){
//     return colorScale(value)
//   })
//   .on('end', function(){
//     d3.select(this)
//     .transition()
//     .duration(1000)
//     .delay(100)
//     .attr('r', function (value) {
//       return Math.random() * 60
//     })
//     .attr('opacity', '0.2')
//
//   })
//

var widthScale = d3.scaleLinear().domain([0, 25]).range([0, 600])
var axis       = d3.axisBottom().scale(widthScale)
var colorScale = d3.scaleLinear().domain([0, 25]).range(['red', 'blue'])

var names = d3.axisLeft()

d3.json('static/resources/posts_data.json').then(function (data){
  var svg =  d3.select('#left')
    .append('svg')
    .attr('width', 600 + 10)
    .attr('height', 600 + 10)
    .attr('transform', 'translate(10,30)')


var bars =  svg.selectAll('rect')
      .data(data)
      .enter()
        .append('rect')
        .attr('transform', 'translate(0, 0)')
        .attr('width', 10)
        .attr('height', 30)
        .attr('y', function(value, i) {
          return i * 50
        })
        .attr('fill', 'black')
        .attr('opacity', '0.7')


bars.transition()
  .delay(100)
  .duration(4000)
  .attr('width', function (value){
      return widthScale(value.posts)
  })
  .attr('fill', function(value){
    return colorScale(value.posts)
  })


  // svg.selectAll('rect')
  //   .data(data)
  //   .enter()
  //     .append('rect')
  //     .attr('transform', 'translate(0, 0)')
  //     .attr('width', function (value){
  //         return widthScale(value.posts)
  //     })
  //     .attr('height', 30)
  //     .attr('y', function(value, i) {
  //       return i * 50
  //     })
  //     .attr('fill', 'red')
  //     .attr('opacity', '0.7')

  svg.selectAll('text')
    .data(data)
    .enter()
      .append('text')
      .attr('fill', 'black')
      .attr('y', function (value, i){
        return i * 50 + 20
      })
      .text(function (value) {
        return value.name
      })
      .attr('transform', 'translate(10, 0)')
      // .attr('height', 30)

  svg.append('g')
    .attr('transform', 'translate(0, 550)')
    .call(axis)

})

var svgWidth = 610, svgHeight = 610, barPadding = 5
var barWidth = (svgWidth/11)

d3.json('static/resources/posts_data.json').then(function (data){
  var svg =  d3.select('#right')
            .append('svg')
            .attr('width', svgWidth)
            .attr('height', svgHeight)

  var barChart = svg.selectAll('rect')
        .data(data)
        .enter()
        .append('rect')
        .attr('y', function(value){
          return svgHeight - value.posts *30
        })
        .attr('height', 10)
        .attr('width', barWidth - barPadding)
        .attr('transform', function (value, i){
          var translate = [barWidth* i, 0]
          return 'translate(' + translate + ')'
        })
        .attr('fill', 'grey')
        .attr('opacity', '0.7')

      barChart.transition()
        .delay(1000)
        .duration(4000)
        .attr('height', function(value){
          return value.posts * 100
        })
        .attr('fill', function (value){
          return colorScale(value.posts)
        })


})



var canvas = d3.select('#middle')
          .attr('width', 610)
          .attr('height', 610)

var xdataset  = [
  {x:10, y:20},
  {x:40, y:60},
  {x:50, y:70}
]

var group= canvas.append('g')
          .attr('transform', 'translate(100, 100)')

var line = d3.svg.line()
      .x(function(value){
        return value.x
      })
      .y(function(value){
        return value.y
      })

group.selectAll('path')
  .data([xdataset])
  .enter()
  .append('path')
  .attr('d', line)
  .attr('fill', 'none')
  .attr('stroke', '#000')
  .attr('stroke-width', 10)

  

//
// //set the dimensions and margins of the graph
// var margin = {top: 30, right: 30, bottom: 70, left: 60},
//     width = 460 - margin.left - margin.right,
//     height = 400 - margin.top - margin.bottom;
//
// // append the svg object to the body of the page
// var svg = d3.select("#left")
//   .append("svg")
//     .attr("width", width + margin.left + margin.right)
//     .attr("height", height + margin.top + margin.bottom)
//   .append("g")
//     .attr("transform",
//           "translate(" + margin.left + "," + margin.top + ")");
//
// // Parse the Data
// d3.json("static/resources/posts_data.json").then(function(data) {
//
// // X axis
// var x = d3.scaleBand()
//   .range([ 0, width ])
//   .domain(data.map(function(d) { return d.name; }))
//   .padding(0.2);

// svg.append("g")
//   .attr("transform", "translate(0," + height + ")")
//   .call(d3.axisBottom(x))
//   .selectAll("text")
//     .attr("transform", "translate(-10,0)rotate(-45)")
//     .style("text-anchor", "end");
//
// // Add Y axis
// var y = d3.scaleLinear()
//   .domain([0, 15])
//   .range([ height, 0]);

// svg.append("g")
//   .call(d3.axisLeft(y))
//
// // Bars
// svg.selectAll("mybar")
//   .data(data)
//   .enter()
//   .append("rect")
//     .attr("x", function(d) { return x(d.name); })
//     .attr("y", function(d) { return y(d.posts); })
//     .attr("width", x.bandwidth())
//     .attr("height", function(d) { return height - y(d.posts); })
//     .attr("fill", "#afc8ab")
//
// })
