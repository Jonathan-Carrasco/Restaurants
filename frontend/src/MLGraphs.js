import React, { Component } from "react";
import * as d3 from 'd3';
import axios from "axios";
import './App.css';

class MLGraphs extends Component {

  /*
  This Component saves arrays containing information on heatmap and
  barchart probabilities, along with the username passed down by the
  parent Component.
  */
  constructor(props) {
      super(props);
      this.state = {
        barchart: [],
        heatmap: []
      };
  }

  /*
  When this Component mounts, we query our barchart and heatmap
  information and display the information visuals. Since creating
  and saving a model for 'username' isn't instantaneous, we must
  wait before retrieving information for the barchart and heatmap.
  */
  componentDidMount() {
    axios.get('/api/users/?username='+this.props.username)
    setTimeout(() => { this.refreshList(); }, 500);
    setTimeout(() => { this.createBarChart();
                       this.createHeatMap();}, 1000);
  }

  componentDidUpdate() {
    this.createBarChart();
    this.createHeatMap();
  }

  refreshList = () => {
    axios
      .get('/api/barcharts/?username='+this.props.username)
      .then(res => this.setState({ barchart: res.data }))
      .catch(err => console.log(err));
    axios
      .get('api/heatmaps/?username='+this.props.username)
      .then(res => this.setState({ heatmap: res.data }))
      .catch(err => console.log(err));
  };

  createBarChart() {
    /* Enumerates all general categories, allowing us to color code our data. */
    const categoryToColor = {'Multicultural': 0,'American': 1,'Latin American': 2,
                        'East Asian': 3,'Southeast Asian':4 ,'Southern European': 5,
                        'Middle Eastern': 6,'Western European': 7,'South Asian': 8,
                        'Northern European': 9,'Central European': 10,'Canadian': 11,
                        'African': 12}

    /* reference to our svg element */
    const node = this.node
    const barchart = this.state.barchart
    const margin = {top: 10, left: 85}
    const height = 600, width = 600;

    /*
    Our y scale takes probabilities ranging from [0,1] and converts
    them to proportional heights ranging from [0,height].
    */
    const yScale = d3.scaleLinear()
       .domain([0,1])
       .range([0, height])

    /* Our Y axis scale is inverted since D3 draws from bottom up. */
    const yScaleAxis = d3.scaleLinear()
       .domain([0,1])
       .range([height,100])

    /* Truncates floats up to 4 decimal points. */
    const formatProbability = d3.format(".4f")

    /* Creates a tooltip div that allows us to display info on hover. */
    const tooltip = d3.select(".container")
      .append('div')
      .attr('class','tooltip')
      .html('Tooltip')

    /* Shifts our svg element accordingly. */
    d3.select(node)
      .attr("transform", "translate("+margin.left+","+margin.top+")")

    /*
    Binds each {category, probability} pair to a reactangle, and positions
    each rectangle 40 pixels up and 50 pixels to the right of our svg.
    */
    d3.select(node)
      .selectAll('rect')
      .data(barchart)
      .enter()
      .append('rect')
      .attr("transform", "translate(50,-40)")

    /*
    Removes extra rectangles created, if the number of barchart categories
    does not match the number of rectangles created.
    */
   d3.select(node)
      .selectAll('rect')
      .data(barchart)
      .exit()
      .remove()

   /*
   Adds color, displays a tooltip on mouseover, and positions each rectangle.

   Colors are assigned by mapping each category to a number and converting
   that number into a hex code.

   On mouseover the category and probabilities are shown.
   */
   d3.select(node)
      .selectAll('rect')
      .data(barchart)
      .style('fill', d => d3.color(d3.interpolateRainbow(categoryToColor[d.category]/12)).hex())
      .attr('x', (d,i) => i * 25)
      .attr('y', d => height - yScale(d.probability) + 10)
      .attr('height', d => yScale(d.probability))
      .attr('width', 25)
      .on('mouseover', (d,i) => {
          tooltip.html('Category: ' + d.category + '<br/> <br/> Probability: ' + formatProbability(d.probability))
            .style('left', '-300px')
            .style('top', '430px')
            .style('opacity', .9);
        }).on('mouseout', () => {
          tooltip.style('opacity', 0)
            .style('left', '0px');
        });

    /*
    A legend is created by adding groups for every category to our DOM.
    */
    var legend = d3.select(node)
            .selectAll(".legend")
            .data(barchart)
            .enter()
            .append("g")

    /*
    Each category is colored in the same manner as above, and the position of
    each category as well as placement of the legened was arbitrarily chosen.
    */
    legend.append("rect")
        .attr("fill", d => d3.color(d3.interpolateRainbow(categoryToColor[d.category]/12)).hex())
        .attr("width", 20)
        .attr("height", 20)
        .attr("y", function (d, i) {
            return i * 25 + 25;
        })
        .attr("x", 410);

    /*
    The names of each category are positioned to the right of the rectangles.
    */
    legend.append("text")
        .attr("class", "label")
        .attr("y", function (d, i) { return i * 25 + 40;})
        .attr("x", 440)
        .attr("text-anchor", "start")
        .text(function (d, i) { return d.category; });

    /*
    Append the y axis, coloring it blue for aesthetical purposes.
    */
    d3.select(node).append('g')
      .attr('transform','translate(50,-30)')
      .style('fill', '#4285F4')
      .attr('class','yAxis')
      .call(d3.axisLeft(yScaleAxis).tickFormat(d3.format('.4')));

    /*
    Append the y axix label, and also color it blue.
    */
    d3.select(node).append('text')
      .attr('transform','translate(15,' + (height / 2)  + ') rotate(-90)')
      .style('text-anchor','middle')
      .style('fill', '#4285F4')
      .text('Probability');

    /*
    Append the x axis label.
    */
    d3.select(node).append('text')
      .attr('transform','translate(220,590)')
      .style('text-anchor','middle')
      .style('fill', '#4285F4')
      .text('Categories');
     }

     createHeatMap() {
          /*
          Initialize an array of probabilities, and arrays of
          [minimum, maximum] pairs.
          */
          const data = this.state.heatmap,
                latitudeRange = d3.extent(data, d => {return d.y }),
                longitudeRange = d3.extent(data, d => {return d.x }),
                probabilityRange = d3.extent(data, d => {return d.probability});

          /* Enumerates all general categories, allowing us to color code our data. */
          const categoryToColor = {'Multicultural': 0,'American': 1,'Latin American': 2,
                              'East Asian': 3,'Southeast Asian':4 ,'Southern European': 5,
                              'Middle Eastern': 6,'Western European': 7,'South Asian': 8,
                              'Northern European': 9,'Central European': 10,'Canadian': 11,
                              'African': 12}

          /* Define the dimensions for this svg element. */
          const width = 450,
                height = 500,
                margins = {top:10, right: 50, bottom: 100, left: 100};

          /*
          Our y scale takes latitudes ranging from [min(lat),max(lat)] and
          converts them to proportional heights ranging from [0,height]. The
          range is inverted since d3 draws from top to bottom.
          */
          const yScale = d3.scaleLinear()
            .domain(latitudeRange)
            .range([height,0]);

          /*
          Our x scale takes longitudes ranging from [min(long),max(long)] and
          converts them to proportional widths ranging from [0,width].
          */
          const xScale = d3.scaleLinear()
            .range([0,width])
            .domain(longitudeRange);

          /*
          Probabilities are formatted in scientific notation and coordinates
          are now accurate up to four decimal places.
          */
          const formatCoordinate = d3.format(".4");
          const formatProbability = d3.format(".0e")

          /* Setting chart width and adjusting for margins */
          const chart = d3.select('.chart')
            .attr('width', width + margins.right + margins.left)
            .attr('height', height + margins.top + margins.bottom)
            .append('g')
            .attr('transform','translate(' + margins.left + ',' + margins.top + ')');

          /* Our heatmap consists of 100x100 squares. */
          const barWidth = width / 100,
                barHeight = height / 100;

          /* Creates a tooltip div that allows us to display info on hover. */
          const tooltip = d3.select('.container').append('div')
            .attr('class','tooltip')
            .html('Tooltip')

          /*
          Adds color, displays a tooltip on mouseover, and positions each rectangle.

          Colors are assigned by mapping each probability to a color spectrum,
          described by d3.interpoalteViridis in D3's documentation. Then, this
          color is converted into a hex code for css style compatibility.

          On mouseover the [latitude,longitude] coordinates are shown, as well as
          their corresponding probability.
          */
          chart.selectAll('g')
            .data(data).enter().append('g')
            .append('rect')
            .attr('x', d => {return xScale(d.x)})
            .attr('y', d => {return yScale(d.y)})
            .style('fill', d => d3.color(d3.interpolateViridis(d.probability)).hex())
            .attr('width', barWidth)
            .attr('height', barHeight)
            .on('mouseover', d => {
                tooltip.html('x: ' + formatCoordinate(d.x) +  margins.right + margins.left + '<br/>y: ' + formatCoordinate(d.y) + margins.top + margins.bottom + '<br/>prob: ' + formatProbability(d.probability))
                  .style('left', xScale(d.x) + 'px')
                  .style('top', yScale(d.y) + 'px')
                  .style('opacity', .9);
              }).on('mouseout', () => {
                tooltip.style('opacity', 0)
                  .style('left', '0px');
              });

          /* Append x axis */
          chart.append('g')
            .attr('transform','translate(0,' + height + ')')
            .style('fill', '#4285F4')
            .call(d3.axisBottom(xScale).tickFormat(d3.format('.4')));

          /* Append y axis */
          chart.append('g')
            .attr('transform','translate(0,-' + (barHeight/2) + ')')
            .call(d3.axisLeft(yScale).tickFormat(d3.format('.4')))
            .attr('class','yAxis')
            .style('fill', '#4285F4');

          /* Append y axis label */
          chart.append('text')
            .attr('transform','translate(-40,' + (height / 2)  + ') rotate(-90)')
            .style('text-anchor','middle')
            .style('fill', '#4285F4')
            .text('Latitude');

          /* Append x axis label */
          chart.append('text')
            .attr('transform','translate(' + (width / 2) + ',' + (height + 40) + ')')
            .style('text-anchor','middle')
            .style('fill', '#4285F4')
            .text('Longitude');

}
    render() {
        return (
                <div class="container-fluid content-row">
                  <div class="row">
                    <div class="col-sm-12 col-lg-6">
                      <div class="card-group">
                        <div class="card h-100 border-primary">
                        <div class="card-body">
                          <svg ref={node => this.node = node} width={600} height={600}></svg>
                        </div>
                        </div>
                      </div>
                    </div>
                    <div class="col-sm-12 col-lg-6">
                        <div class="card h-100 border-primary">
                        <div class="card-body">
                            <div className='container'>
                              <svg className='chart'></svg>
                            </div>
                        </div>
                        </div>
                      </div>
                  </div>
                </div>
        )
    }

}


export default MLGraphs
