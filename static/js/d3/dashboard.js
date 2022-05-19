d3.select()
d3.selectAll()
var monJson = [{ "name": "Ervin Howell", "nbr": 1 }, { "name": "Leanne Graham", "nbr": 5 }, { "name": "Patricia Lebsack", "nbr": 7 }, { "name": "Clementine Bauch", "nbr": 11 }, { "name": "Mrs. Dennis Schulist", "nbr": 10 }, { "name": "Nicholas Runolfsdottir V", "nbr": 6 }, { "name": "Glenna Reichert", "nbr": 10 }, { "name": "Clementina DuBuque", "nbr": 2 }, { "name": "Chelsey Dietrich", "nbr": 10 }, { "name": "Kurtis Weissnat", "nbr": 12 }]
var data = [10, 20, 30, 20, 10];
var width = 400;
var height = 400;
var widthScale = d3.scaleLinear().domain([0, 15]).range([0, width]);
var color = d3.scaleLinear().domain([0, 12]).range(["red", "blue"]);
// var axis = d3.svg.axis().scale(widthScale);

// selecting the div 
var svg1 = d3.select('#svg1div')
    .append('svg')
    .attr('width', 400)
    .attr('height', 400)
    .append("g")
    .attr("transform", "translate(20, 0)");
// creating our chart's containt
var bars = svg1.selectAll("rect")
    .data(monJson)
    .enter()
    .append("rect")
    .attr("width", function(d) {
        return widthScale(d.nbr);
    })
    .attr("height", 30)
    .attr("fill", function(d) { return color(d.nbr) })
    .attr("y", function(d, i) { return i * 40 });

// data = [1, 10, 20, 30, 40, 50, 60, 70]
// var monJson = [{ "name": "Ervin Howell", "nbr": 10 }, { "name": "Leanne Graham", "nbr": 10 }, { "name": "Patricia Lebsack", "nbr": 10 }, { "name": "Clementine Bauch", "nbr": 11 }, { "name": "Mrs. Dennis Schulist", "nbr": 10 }, { "name": "Nicholas Runolfsdottir V", "nbr": 10 }, { "name": "Glenna Reichert", "nbr": 10 }, { "name": "Clementina DuBuque", "nbr": 0 }, { "name": "Chelsey Dietrich", "nbr": 10 }, { "name": "Kurtis Weissnat", "nbr": 12 }]

// var colorScale = d3.scaleLinear()
//     .domain([0, 68])
//     .range(['red', 'blue'])

// var heightScale = d3.scaleLinear()
//     .domain([1, 70])
//     .range([0, 300])


// var axis = d3.axisRight().scale(heightScale)

// var svg = d3.select('#svg1div')
//     .append('svg')
//     .attr('width', 400)
//     .attr('height', 400)


// svg.append('g')
//     .attr('transform', 'translate(20, 0)')
//     .call(axis)


// svg.selectAll('rect')
//     .data(monJson)
//     .enter()
//     // ajoute un element rect dans le svg
//     .append('rect')
//     .attr('x', function(data, i) {
//         return data.nbr * 20
//     })
//     // permet de translater les rectangles suivant la valeur dans note jeu de donnees data
//     .attr('transform', function(data, i) {
//         var translate = [data.nbr * 2, 0]
//         return 'translate(' + translate + ')'
//     })
//     .attr('y', function(data, i) {
//         return 0
//     })
//     .attr('width', 20)
//     .attr('height', 0)
//     .attr('fill', 'black')


// // pour faire une transition
// svg.selectAll('rect')
//     .transition()
//     .delay(2000)
//     .duration(4000)
//     .attr('height', function(data, i) {
//         return heightScale(data.nbr)
//     })
//     .attr('fill', function(data, i) {
//         return colorScale(data.nbr)
//     })


// SECOND Grav///////////////////

var edf = [
    { 'name': 'Mrs. Dennis Schulist', 'nbr': 10 },
    { 'title': 'ullam ut quidem id aut vel consequuntur', 'nbr': 5 },
    { 'title': 'doloremque illum aliquid sunt', 'nbr': 5 },
    { 'title': 'qui explicabo molestiae dolorem', 'nbr': 5 },
    { 'title': 'magnam ut rerum iure', 'nbr': 5 },
    { 'title': 'id nihil consequatur molestias animi provident', 'nbr': 5 },
    { 'title': 'fuga nam accusamus voluptas reiciendis itaque', 'nbr': 5 },
    { 'title': 'provident vel ut sit ratione est', 'nbr': 5 },
    { 'title': 'explicabo et eos deleniti nostrum ab id repellendus', 'nbr': 5 },
    { 'title': 'eos dolorem iste accusantium est eaque quam', 'nbr': 5 },
    { 'title': 'enim quo cumque', 'nbr': 5 },
    { 'title': 'asperiores ea ipsam voluptatibus modi minima quia sint', 'nbr': 5 },
    { 'title': 'dolor sint quo a velit explicabo quia nam', 'nbr': 5 },
    { 'title': 'maxime id vitae nihil numquam', 'nbr': 5 },
    { 'title': 'autem hic labore sunt dolores incidunt', 'nbr': 5 },
    { 'title': 'rem alias distinctio quo quis', 'nbr': 5 },
    { 'title': 'est et quae odit qui non', 'nbr': 5 },
    { 'title': 'quasi id et eos tenetur aut quo autem', 'nbr': 5 },
    { 'title': 'delectus ullam et corporis nulla voluptas sequi', 'nbr': 5 },
    { 'title': 'iusto eius quod necessitatibus culpa ea', 'nbr': 5 },
    { 'title': 'a quo magni similique perferendis', 'nbr': 5 },
    { 'title': 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit', 'nbr': 5 },
    { 'title': 'qui est esse', 'nbr': 5 },
    { 'title': 'ea molestias quasi exercitationem repellat qui ipsa sit aut', 'nbr': 5 },
    { 'title': 'eum et est occaecati', 'nbr': 5 },
    { 'title': 'nesciunt quas odio', 'nbr': 5 },
    { 'title': 'dolorem eum magni eos aperiam quia', 'nbr': 5 },
    { 'title': 'magnam facilis autem', 'nbr': 5 },
    { 'title': 'dolorem dolore est ipsam', 'nbr': 5 },
    { 'title': 'nesciunt iure omnis dolorem tempora et accusantium', 'nbr': 5 },
    { 'title': 'optio molestias id quia eum', 'nbr': 5 },
    { 'title': 'Démo', 'nbr': 0 },
    { 'title': 'et ea vero quia laudantium autem', 'nbr': 5 },
    { 'title': 'in quibusdam tempore odit est dolorem', 'nbr': 5 },
    { 'title': 'dolorum ut in voluptas mollitia et saepe quo animi', 'nbr': 5 },
    { 'title': 'voluptatem eligendi optio', 'nbr': 5 },
    { 'title': 'eveniet quod temporibus', 'nbr': 5 },
    { 'title': 'sint suscipit perspiciatis velit dolorum rerum ipsa laboriosam odio', 'nbr': 5 },
    { 'title': 'fugit voluptas sed molestias voluptatem provident', 'nbr': 5 },
    { 'title': 'voluptate et itaque vero tempora molestiae', 'nbr': 5 },
    { 'title': 'adipisci placeat illum aut reiciendis qui', 'nbr': 5 },
    { 'title': 'doloribus ad provident suscipit at', 'nbr': 5 },
    { 'title': 'non est facere', 'nbr': 5 },
    { 'title': 'commodi ullam sint et excepturi error explicabo praesentium voluptas', 'nbr': 5 },
    { 'title': 'eligendi iste nostrum consequuntur adipisci praesentium sit beatae perferendis', 'nbr': 5 },
    { 'title': 'optio dolor molestias sit', 'nbr': 5 },
    { 'title': 'ut numquam possimus omnis eius suscipit laudantium iure', 'nbr': 5 },
    { 'title': 'aut quo modi neque nostrum ducimus', 'nbr': 5 },
    { 'title': 'quibusdam cumque rem aut deserunt', 'nbr': 5 },
    { 'title': 'ut voluptatem illum ea doloribus itaque eos', 'nbr': 5 },
    { 'title': 'laborum non sunt aut ut assumenda perspiciatis voluptas', 'nbr': 5 },
    { 'title': 'repellendus qui recusandae incidunt voluptates tenetur qui omnis exercitationem', 'nbr': 5 },
    { 'title': 'soluta aliquam aperiam consequatur illo quis voluptas', 'nbr': 5 },
    { 'title': 'qui enim et consequuntur quia animi quis voluptate quibusdam', 'nbr': 5 },
    { 'title': 'ut quo aut ducimus alias', 'nbr': 5 },
    { 'title': 'sit asperiores ipsam eveniet odio non quia', 'nbr': 5 },
    { 'title': 'sit vel voluptatem et non libero', 'nbr': 5 },
    { 'title': 'qui et at rerum necessitatibus', 'nbr': 5 },
    { 'title': 'sed ab est est', 'nbr': 5 },
    { 'title': 'voluptatum itaque dolores nisi et quasi', 'nbr': 5 },
    { 'title': 'qui commodi dolor at maiores et quis id accusantium', 'nbr': 5 },
    { 'title': 'consequatur placeat omnis quisquam quia reprehenderit fugit veritatis facere', 'nbr': 5 },
    { 'title': 'voluptatem doloribus consectetur est ut ducimus', 'nbr': 5 },
    { 'title': 'beatae enim quia vel', 'nbr': 5 },
    { 'title': 'voluptas blanditiis repellendus animi ducimus error sapiente et suscipit', 'nbr': 5 },
    { 'title': 'et fugit quas eum in in aperiam quod', 'nbr': 5 },
    { 'title': 'consequatur id enim sunt et et', 'nbr': 5 },
    { 'title': 'repudiandae ea animi iusto', 'nbr': 5 },
    { 'title': 'aliquid eos sed fuga est maxime repellendus', 'nbr': 5 },
    { 'title': 'odio quis facere architecto reiciendis optio', 'nbr': 5 },
    { 'title': 'fugiat quod pariatur odit minima', 'nbr': 5 },
    { 'title': 'voluptatem laborum magni', 'nbr': 5 },
    { 'title': 'et iusto veniam et illum aut fuga', 'nbr': 5 },
    { 'title': 'sint hic doloribus consequatur eos non id', 'nbr': 5 },
    { 'title': 'consequuntur deleniti eos quia temporibus ab aliquid at', 'nbr': 5 },
    { 'title': 'enim unde ratione doloribus quas enim ut sit sapiente', 'nbr': 5 },
    { 'title': 'dignissimos eum dolor ut enim et delectus in', 'nbr': 5 },
    { 'title': 'doloremque officiis ad et non perferendis', 'nbr': 5 },
    { 'title': 'necessitatibus quasi exercitationem odio', 'nbr': 5 },
    { 'title': 'quam voluptatibus rerum veritatis', 'nbr': 5 },
    { 'title': 'pariatur consequatur quia magnam autem omnis non amet', 'nbr': 5 },
    { 'title': 'labore in ex et explicabo corporis aut quas', 'nbr': 5 },
    { 'title': 'tempora rem veritatis voluptas quo dolores vero', 'nbr': 5 },
    { 'title': 'laudantium voluptate suscipit sunt enim enim', 'nbr': 5 },
    { 'title': 'odit et voluptates doloribus alias odio et', 'nbr': 5 },
    { 'title': 'optio ipsam molestias necessitatibus occaecati facilis veritatis dolores aut', 'nbr': 5 },
    { 'title': 'dolore veritatis porro provident adipisci blanditiis et sunt', 'nbr': 5 },
    { 'title': 'placeat quia et porro iste', 'nbr': 5 },
    { 'title': 'nostrum quis quasi placeat', 'nbr': 5 },
    { 'title': 'sapiente omnis fugit eos', 'nbr': 5 },
    { 'title': 'sint soluta et vel magnam aut ut sed qui', 'nbr': 5 },
    { 'title': 'ad iusto omnis odit dolor voluptatibus', 'nbr': 5 },
    { 'title': 'Posts', 'nbr': 0 },
    { 'title': 'Je pense', 'nbr': 0 }
]

var svg2 = d3.select("#svg2div")
    .append("svg")
    .attr('height', 400)
    .attr('width', 400);
var circle = svg2.append("circle")
    .attr("cx", 250)
    .attr("cy", 250)
    .attr("r", 150)
    .attr('fill', "aqua")

// THIRD
var svg3 = d3.select("svg3div")