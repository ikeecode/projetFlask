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
var colorScale1 = d3.scaleSequential().domain([0, 25]).interpolator(d3.interpolateRainbow)

var names = d3.axisLeft()


// le premier diagramme
d3.json('static/resources/posts_data.json').then(function (data){
  // creation du svg
  var svg =  d3.select('#left')
    .append('svg')
    .attr('width', 600 + 10 + 10)
    .attr('height', 600 + 10)
    .attr('transform', 'translate(3 ,8)')


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
    .delay(500)
    .duration(4000)
    .attr('width', function (value){
        return widthScale(value.posts)
    })
    .attr('fill', function(value){
      return colorScale1(value.posts)
    })

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

  svg.append('g')
    .attr('transform', 'translate(0, 550)')
    .call(axis)

  svg.append('g')
    .append('text')
    .text('(le nombre de posts/user)')
    .attr('transform', 'translate(50, -50)')
    .style('color', 'grey')
    .attr('transform', 'translate(440, 540)')



})



// le deuxieme diagramme
var svgWidth = 610, svgHeight = 610, barPadding = 5
var barWidth = (svgWidth/11)
var rightAxis   = d3.axisRight().scale(widthScale)

d3.json('static/resources/posts_data.json').then(function (data){
  var names = new Array()

  data.forEach((item) => {
    names.push(item.name)
  })

  // var nameScale = d3.scaleLinear().domain(names).range([0, svgWidth])
  // var bottomAxis = d3.axisBottom().scale(nameScale)
  // bottomAxis.tickValues = names
  var svg =  d3.select('#right')
            .append('svg')
            .attr('width', svgWidth)
            .attr('height', svgHeight + 30)
            .attr('transform', 'translate(30, -40)')

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

      barChart.selectAll('text')
        .data(data)
        .enter()
          .append('text')
          .text(function (value){
            return value.name
          })
          .attr('transform', `translate(${svgWidth},${svgHeight})`)
          .attr('fill', 'black')
          // .attr('transform', 'rotate(-180deg)')
          .attr('y', function (value, i){
            return i * 50
          })


      barChart.transition()
        .delay(500)
        .duration(4000)
        .attr('height', function(value){
          return value.posts * 100
        })
        .attr('fill', function (value){
          return colorScale1(value.posts)
        })

      svg.append('g')
          .attr('transform', `translate( ${svgWidth - barPadding}, 35)`)
          .call(rightAxis)
})




// troisieme graphe : diagramme circulaire
//
// d3.json('static/resources/posts_data.json').then(function (data){
//     var svg = d3.select('')
//               .append('svg')
//               .attr('width', 610)
//               .attr('height', 610)
//
//     var group = svg.append('g')
//                 .attr('transform', 'translate(305, 305)')
//
//     var xdata = new Array()
//     var names = new Array()
//
//     data.forEach((item) => {
//       xdata.push(item.posts)
//       names.push(item.name)
//     })
//
//     var pie = d3.pie()
//     var arcs = pie(xdata)
//     // console.log(arcs)
//
//     var archer = d3.arc()
//         .innerRadius(20)
//         .outerRadius(230)
//
//
//   group.selectAll('path')
//       .data(arcs)
//       .enter()
//         .append('path')
//         .attr('d', archer)
//         .attr('fill', 'pink')
//         .attr('stroke', 'white')
// })

d3.json('static/resources/comments_per_posts.json').then(function(data){
  var svgWidth = 610, svgHeight = 610, radius = Math.min(svgWidth, svgHeight) /2 - 50
  var svg = d3.select('#left-1')
    .append('svg')
    .attr('width', svgWidth)
    .attr('height', svgHeight)



  var g = svg.append('g')
      .attr('transform', 'translate(305, 305)')
      // .attr('transform', `translate('${radius}, ${radius}')`)

  var color = d3.scaleOrdinal(d3.schemeCategory10)

  var pie = d3.pie().value(function(d){
    return d.comments
  })

  var path = d3.arc()
      .outerRadius(radius)
      .innerRadius(70)

  var path1 = d3.arc()
          .outerRadius(radius)
          .innerRadius(30)

  var arc = g.selectAll('arc')
    .data(pie(data))
    .enter()
    .append('g')

  path2 = 'M60,-100A1,1,0,0,1,3,8'
  arc.append('path')
    .attr('d', path)
    .attr('fill', function(d){
      return color(d.data.comments * Math.random() * 10)
    })
    .attr('stroke', 'white')
    .attr('stroke-width', 25)
    .append('animateMotion')
    .attr('dur', '5s')
    .attr('repeatCount', '1')
    .attr('path', path2)

  arc.selectAll('path')
    .transition()
    .delay(500)
    .duration(7000)
    .attr('d', path1)
    .attr('stroke-width', 3)


})


// cercles

d3.json('static/resources/comments_per_posts.json').then(function (data){
  var svg = d3.select('#right-1')
            .append('svg')
            .attr('width', 640)
            .attr('height', 610)

  var group = svg.append('g')
            .attr('transform', 'translate(0, 305)')
            // .append('line')

  var positions = new Array()
  data.forEach((item, i) => {
    positions.push(i)
  })
  props = [-1, 1]

var circles = group.append('g')
    .selectAll('circle')
    .data(data)
    .enter()
      .append('circle')
      .attr('r', function (value){
        return Math.random() * Math.PI * Math.random() * 10
      })
      .attr('opacity', 0.2)
      .attr('cx', function (value, i){
        return Math.random() * 200 *(Math.random() * 20)
      })
      .attr('cy', function (value, i){
        return Math.random() * 200 *(Math.random() * 20) * props[Math.floor(Math.random() * 2)]
      })
      // .attr('cy', function(value){
      //   return Math.random() * 100
      // })
      .attr('fill', function(value){
        return colorScale1(value.comments *5)
      })
      .attr('stroke', 'black')
      .attr('transform', function(value, i){
        var translate = [Math.random() * 100, 100* Math.random()]
        return  'translate(' + translate + ')'
      })

// transition circles

circles.transition()
  .delay(300)
  .duration(7000)
  .attr('r', function (value){
    return value.comments * 10
  })
  .attr('opacity', 0.5)
  .attr('cx', function (value, i){
    if (i==0) return 20
    return positions[i] * 50
  })
  .attr('cy', 1)
  .attr('transform', function(value, i){
    var translate = [10*i + 10, 10]
    return  'translate(' + translate + ')'
  })
  .attr('stroke', 'white')




      group.append('line')
          // .attr('transform', 'translate(300, 10)')
          .attr('x1', 250)
          .attr('y1', 10)
          .attr('x2', 250)
          .attr('y2', 10)
          .attr('fill', 'black')
          .attr('stroke', 'black')

      // line transition
      group.select('line')
          .transition()
          .delay(300)
          .duration(3000)
          .attr('x1', 30)
          .attr('y1', 10)
          .attr('x2', positions.pop() * 60 + 6)
          .attr('y2', 10)
          .attr('fill', 'black')
          .attr('stroke', 'black')



  // group.selectAll('line')
  //   .data(data)
  //   .enter()
  //     .append('line')
  //     .attr('x1', function (value, i){
  //       if (i==0) return 20
  //       return positions[i] * 50
  //     })
  //     .attr('y1', 1)
  //     .attr('x2', function (value, i){
  //       if (i==0) return 20
  //       return positions[i] * 50
  //     })
  //     .attr('y2', 100)
  //     .attr('stroke', 'black')
  //     .attr('fill', 'black')
  //     .attr('stroke-width', 1)
  //     .attr('transform', function(value, i){
  //       var translate = [10*i + 10, 10]
  //       return  'translate(' + translate + ')'
  //     })
})


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
