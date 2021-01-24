let data_source, metric_selected, model_list, split_formation, split_number, weighting, sts_percentage

window.addEventListener('load', () => {
    console.log('Window loaded');
    draw()
})

function draw(){
    d3.select("#select7m").on("change",function(){
        d3.selectAll(".woodsts").style("opacity","0.25")
        d3.selectAll(".biassts").style("opacity","0.25")

        metric_selected=d3.select(this).property("value")
        if(metric_selected=='WOOD'){
            d3.selectAll(".woodsts").style("opacity","1")
        }
        else{
            d3.selectAll(".woodsts").style("opacity","0.25")
        }    
        if(metric_selected=='WSBias'){
            d3.selectAll(".biassts").style("opacity","1")
        }
        else{
            d3.selectAll(".biassts").style("opacity","0.25")
        }    
    })

    d3.select("#submitctrl").on("click",function(){
        data_source=d3.select("#select7d").property("value")
        metric_selected=d3.select("#select7m").property("value")
        model_list=d3.select("#modelrank").property("value")
        split_formation=d3.select("#select7").property("value")
        split_number=d3.select("#selectno").property("value")
        weighting=d3.select("#selectws").property("value")
        sts_percentage=d3.select("#selectwood").property("value")
        weight_factor=d3.select("#selectw").property("value")
        bias_algo=d3.select("#selectbias").property("value")
        makeplots(data_source, metric_selected, model_list, split_formation, split_number, weighting, sts_percentage,weight_factor,bias_algo)
    })
}

function makeplots(data_source, metric_selected, model_list, split_formation, split_number, weighting, sts_percentage,weight_factor,bias_algo){
console.log(data_source, metric_selected, model_list, split_formation, split_number, weighting, sts_percentage,weight_factor,bias_algo)
    $.ajax({
        type : "POST",
        url : '/update',
        data: JSON.stringify( {data_source, metric_selected, model_list, split_formation, split_number, weighting, sts_percentage, weight_factor,bias_algo}),
        contentType: 'application/json;charset=UTF-8',
        success: function (fpath) {
            beeswarm(fpath)
            splitwisescatter('./static/data/plotting/splitwise-'+data_source+'-'+metric_selected+'-'+split_formation+'-'+split_number+'-'+weighting+'-'+sts_percentage+'-'+weight_factor+'-'+bias_algo+'.csv')
            accscatter('./static/data/plotting/acc-'+data_source+'-'+metric_selected+'-'+split_formation+'-'+split_number+'-'+weighting+'-'+sts_percentage+'-'+weight_factor+'-'+bias_algo+'.csv')
            sun('./static/data/plotting/sun-'+data_source+'-'+metric_selected+'-'+split_formation+'-'+split_number+'-'+weighting+'-'+sts_percentage+'-'+weight_factor+'-'+bias_algo+'.csv')
            }
        });    

}

function beeswarm(fpath){
    d3.select("#bee").remove()
    d3.csv(fpath,function(data) {
        bee_data=[]
        data.forEach(function(d){
                bee_data.push(Object.entries(d))
        });                
        var bee_width=+d3.select('.centertop').style('width').split('p')[0]
        var bee_height=+d3.select('.centertop').style('height').split('p')[0]
        var bee_margin = {top: 20, bottom: 20, left: 20, right:20}
        var bee_svg = d3.select('.centertop').append('svg').attr('width', bee_width).attr('height', bee_height).attr('id','bee')
        bee_svg=bee_svg.append('g').attr("width",bee_width-bee_margin.left-bee_margin.right).attr("height",bee_height-bee_margin.top-bee_margin.bottom)
                    .attr('transform', "translate("+bee_margin.left+","+bee_margin.top+")")

        var labels=model_list.split('\n')
        var xScale = d3.scalePoint().domain(labels).range([0, bee_width-bee_margin.left-bee_margin.right]).padding(0.5);
        var xAxis=d3.axisBottom().scale(xScale)
        bee_svg.append("g").attr("transform", "translate(10," + (bee_height-40)+ ")").call(xAxis).style("font-size","11px").style("font-weight","bold")
        var yScale = d3.scaleLinear().domain([0, 1]).range([bee_height-bee_margin.top-bee_margin.bottom, 0])
        var yAxis = d3.axisLeft().scale(yScale).tickValues([.25, .5, .75, 1]).tickFormat(d3.format(".2f")); 
        bee_svg.append("g").attr("transform", "translate(10, 0)").call(yAxis).style("font-size","11px").style("font-weight","bold")

        var tooltip = d3.select("body")
        .append("div")
        .style("position", "absolute")
        .style("opacity", ".8")
        .style("visibility", "hidden")
        .style("color","white")
        .style("background-color", "black")
            .style("border-radius", "2px")
        .style("padding", "5px")
        .style("font-family","sans-serif")
        .style("font-size","12px")
        ;

        var beeswarm=[]
        if(metric_selected!='WMProb'){
            var mod=model_list.split('\n')
            for(i=0;i<bee_data.length;i++){
                for(m=0;m<mod.length;m++){
                    var dstatus,dscore,did,dsplit
                    for(k=0;k<bee_data[i].length;k++){
                        if(bee_data[i][k][0]==mod[m]+'_factor'){
                            dstatus=(parseFloat(bee_data[i][k][1])>=0)?'Correct':'Incorrect'
                        }
                        if(bee_data[i][k][0]=='val'){dscore=parseFloat(bee_data[i][k][1])}
                        if(bee_data[i][k][0]=='ID'){did=parseFloat(bee_data[i][k][1])}
                        if(bee_data[i][k][0]=='split'){dsplit=+bee_data[i][k][1]}
                    }
                    obj={'Label':mod[m],'Score':dscore,'ID':did,'Status':dstatus,'Split':dsplit,'x':xScale(mod[m])+10,'y':yScale(dscore)}
                    beeswarm.push(obj)
                }
            }  
        }
        else{
            var mod=model_list.split('\n')
            var beeswarm=[]
            for(i=0;i<bee_data.length;i++){
                for(m=0;m<mod.length;m++){
                    var dstatus,dscore,did,dsplit
                    for(k=0;k<bee_data[i].length;k++){
                        if(bee_data[i][k][0]==mod[m]+'_factor'){dstatus=(parseFloat(bee_data[i][k][1])>=0)?'Correct':'Incorrect'}
                        if(bee_data[i][k][0]==mod[m]+'-val'){dscore=parseFloat(bee_data[i][k][1])}
                        if(bee_data[i][k][0]==mod[m]+'_id'){did=parseFloat(bee_data[i][k][1])}
                        if(bee_data[i][k][0]==mod[m]+'-split'){dsplit=+bee_data[i][k][1]}
                    }
                    obj={'Label':mod[m],'Score':dscore,'ID':did,'Status':dstatus,'Split':dsplit,'x':xScale(mod[m])+10,'y':yScale(dscore)}
                    beeswarm.push(obj)
                }
            }  
        }


        var nodes=bee_svg.append('g').selectAll('dot').data(beeswarm).enter().append('circle')
            .attr('class','circ')
            .attr('id',function(d){return "c-"+d.Split+"-"+d.Label+"-"+d.ID})
            .attr("r","4")
            .attr("cx",function(d){return 10+xScale(d.Label)})
            .attr("cy",function(d){return yScale(d.Score)})
            .attr("stroke","black")
            .attr("stroke-width",1)
            .attr("fill",function(d){
                if (d.Status == "Incorrect"){ return "#fb8072";}
                else if (d.Status == "Correct"){ return "#8dd3c7";}
                return "transparent";
            })
            .on('mouseover', function(d){
                var sco
                if(metric_selected=='WMProb'){sco='MProb'}
                else if(metric_selected=='WOOD'){sco='STS'}
                else if(metric_selected=='WSBias'){sco='Bias'}
                tooltip.html("<center><strong>"+sco+": "+d.Score.toFixed(4)+"</center>");
                return tooltip.style("visibility", "visible");
                    }
            )
            .on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
            .on("mouseout", function(){return tooltip.style("visibility", "hidden");});
        d3.selectAll('#controls').remove()
        var controls = d3.select(".righttop").append("label").attr("id", "controls").style("position","absolute").style("top",160).style("left",1502);
        var controls1 = d3.select(".righttop").append("label").attr("id", "controls").style("position","absolute").style("top",190).style("left",1522);
        var cb1=controls.append('input').attr('type', 'checkbox').attr("id", "splitcheck")
        cb1.on('change',function(){
            var splitcolor=["#8dd3c7","#ffffb3","#bebada","#fb8072","#80b1d3","#fdb462","#b3de69","#fccde5","#d9d9d9","#bc80bd","#ccebc5","#ffed6f"]
            if(cb1.node().checked){
                bee_svg.selectAll('.circ')
                        .attr("r",function(d){if(d.Status=='Incorrect'){return "2"} return "4"})                
                        .attr("fill",function(d){
                            return splitcolor[d.Split];
                        })       
            }
            else{
                bee_svg.selectAll('.circ').attr("r","4")
                .attr("fill",function(d){
                    if (d.Status == "Incorrect"){ return "#fb8072";}
                    else if (d.Status == "Correct"){ return "#8dd3c7";}
                    return "transparent";
                })

            }
        })
        controls.append("text").style("font-size","11px").text("Show Splits")
        var cb2=controls.append('input').attr('type', 'checkbox').attr("id", "forcecheck")
        cb2.on('change',function(){
            if(cb2.node().checked){
                var xValue=function(d){return xScale(d.Label)+10};
                var yValue=function(d){return yScale(d.Score)};      
                var force = d3.forceSimulation(beeswarm)
                    .force("x", d3.forceX(xValue))
                    .force("y", d3.forceY(yValue))
                    .force("collide", d3.forceCollide().radius(5))
                    .on("tick", tickActions)

                function tickActions(e) {
                    nodes
                        .attr("cx", function(d, i) { return Math.max(4,Math.min(bee_width-bee_margin.left-bee_margin.right-4,d.x)); })
                        .attr("cy", function(d, i) { return Math.max(4,Math.min(bee_height-bee_margin.top-bee_margin.bottom-4,d.y)); });
                } 
            }
            else{
                bee_svg.selectAll('.circ').attr("r","4")
                .attr("cx",function(d){return 10+xScale(d.Label)})
                .attr("cy",function(d){return yScale(d.Score)})        
            }
            })
        controls.append("text").style("font-size","11px").text("Collision Detection")                
        controls1.append("text").style("font-size","11px").text("Display: ")                
        var cb3=controls1.append('select').attr("id", "splitshow").style('width',115).style('position','relative').style('left',3)
        var xsplit=['All Splits']
        for(i=1;i<=split_number;i++){
            xsplit.push(i)
        }
        d3.select("#splitshow")
        .selectAll('myOptions')
           .data(xsplit)
        .enter()
          .append('option')
        .text(function (d) { if(d=='All Splits'){return 'All Splits'} console.log('Split '+d);return 'Split '+d; })
        .attr("value", function (d) { if(d=='All Splits'){return 0} return d; })
        cb3.on('change',function(){
            var choice=d3.select('#splitshow').property("value")
            if(choice==0){
                bee_svg.selectAll('.circ').style('visibility','visible')
            }
            else{
                bee_svg.selectAll('.circ').style('visibility',function(d){if(d.Split==choice){return 'visible'} return 'hidden'})
            }
        })
        console.log(beeswarm)
        console.log(bee_data,data)
    });
}

function splitwisescatter(fpath){

    d3.select("#beesws").remove()
    d3.csv(fpath,function(data) {
        var exarr=[]
        data.forEach(function(d){
                d.Score=parseFloat(d.Score).toFixed(4)
                d.Split=+d.Split
                exarr.push(parseFloat(d.Score))
        });
        var extent=d3.extent(exarr)               
        console.log(data,extent)
        extent[0]=extent[0]-0.05
        extent[0]=extent[0]+0.05
        var bee_width=+d3.select('.centerb1').style('width').split('p')[0]
        var bee_height=+d3.select('.centerb1').style('height').split('p')[0]
        var bee_margin = {top: 20, bottom: 20, left: 20, right:20}
        var bee_svg = d3.select('.centerb1').append('svg').attr('width', bee_width).attr('height', bee_height).attr('id','beesws')
        bee_svg=bee_svg.append('g').attr("width",bee_width-bee_margin.left-bee_margin.right).attr("height",bee_height-bee_margin.top-bee_margin.bottom)
                    .attr('transform', "translate("+bee_margin.left+","+bee_margin.top+")")
        
        var xsplit=[]
        for(i=1;i<=split_number;i++){
            xsplit.push(i)
        }
        var xScale = d3.scalePoint().domain(xsplit).range([0, bee_width-bee_margin.left-bee_margin.right]).padding(0.5);
        var xAxis=d3.axisBottom().scale(xScale)
        bee_svg.append("g").attr("transform", "translate(10," + (bee_height-40)+ ")").call(xAxis).style("font-size","11px").style("font-weight","bold")
        var yScale = d3.scaleLinear().domain(extent).range([bee_height-bee_margin.top-bee_margin.bottom, 0])
        var yAxis = d3.axisLeft().scale(yScale).ticks(4).tickFormat(d3.format(".2f")); 
        bee_svg.append("g").attr("transform", "translate(10, 0)").call(yAxis).style("font-size","11px").style("font-weight","bold")

        function make_x_gridlines() {		
            return d3.axisBottom(xScale)
                .ticks(split_number)
        }
        function make_y_gridlines() {		
            return d3.axisLeft(yScale)
                .ticks(4)
        }
        bee_svg.append("g")			
        .attr("class", "grid")
        .attr("transform", "translate(10," + (bee_height-40)+ ")")
            .call(make_x_gridlines()
            .tickSize(-(bee_height-bee_margin.top-bee_margin.bottom))
            .tickFormat("")
        ).style('stroke','lightgrey').style('stroke-opacity',0.2)  
        bee_svg.append("g")			
            .attr("class", "grid")
            .call(make_y_gridlines()
                .tickSize(-(bee_width-bee_margin.left-bee_margin.right))
                .tickFormat("")
            ).attr("transform", "translate(10, 0)")
            .style('stroke','lightgrey').style('stroke-opacity',0.2)


        var tooltip = d3.select("body")
        .append("div")
        .style("position", "absolute")
        .style("opacity", ".8")
        .style("visibility", "hidden")
        .style("color","white")
        .style("background-color", "black")
            .style("border-radius", "2px")
        .style("padding", "5px")
        .style("font-family","sans-serif")
        .style("font-size","12px")
        ;

        var mcolor=["#8dd3c7","#bebada","#fb8072","#80b1d3","#fdb462","#b3de69","#fccde5","#d9d9d9","#bc80bd","#ccebc5","#ffed6f"]
        var mod=model_list.split('\n')
        bee_svg.append('g').selectAll('dot').data(data).enter().append('circle')
            .attr('class','circ')
            .attr('id',function(d){return "c-"+d.Split+"-"+d.Label})
            .attr("r","7")
            .attr("cx",function(d){return 10+xScale(d.Split)})
            .attr("cy",function(d){return yScale(parseFloat(d.Score))})
            .attr("stroke","black")
            .attr("stroke-width",1)
            .attr("fill",function(d){var ind; for(i=0;i<mod.length;i++){if(mod[i]==d.Label){ind=i}} return mcolor[ind]})
            .on('mouseover', function(d){
                tooltip.html("<center><strong>"+d.Label+": "+d.Score+"</center>");
                return tooltip.style("visibility", "visible");
                }
            )
            .on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
            .on("mouseout", function(){return tooltip.style("visibility", "hidden");});

        for(i=0;i<mod.length;i++){
            for(j=0;j<xsplit.length-1;j++){
                var x1=d3.select("#c-"+xsplit[j]+'-'+mod[i]).attr("cx")
                var y1=d3.select("#c-"+xsplit[j]+'-'+mod[i]).attr("cy")
                var x2=d3.select("#c-"+xsplit[j+1]+'-'+mod[i]).attr("cx")
                var y2=d3.select("#c-"+xsplit[j+1]+'-'+mod[i]).attr("cy")
                bee_svg.append('line')
                .style("stroke", mcolor[i])
                .style("stroke-width", 3)
                .attr("x1", x1)
                .attr("y1", y1)
                .attr("x2", x2)
                .attr("y2", y2);         
            }
        }        
    });
}

function accscatter(fpath){

    d3.select("#beeacc").remove()
    d3.csv(fpath,function(data) {
        var exarr=[],mod=[]
        data.forEach(function(d){
                d.Acc=parseFloat(d.Acc).toFixed(4)
                d.Score=parseFloat(d.Score).toFixed(4)
                exarr.push(parseFloat(d.Acc))
                exarr.push(parseFloat(d.Score))
                mod.push(d.Model)
                console.log(d.Model,d.WModel)
        });
        var extent=d3.extent(exarr)               
        extent[0]=extent[0]-5
        extent[1]=extent[1]+5
        console.log(data,extent)
        var bee_width=+d3.select('.centerb2').style('width').split('p')[0]
        var bee_height=+d3.select('.centerb2').style('height').split('p')[0]
        var bee_margin = {top: 20, bottom: 80, left: 20, right:20}
        var bee_svg = d3.select('.centerb2').append('svg').attr('width', bee_width).attr('height', bee_height).attr('id','beeacc')
        bee_svg=bee_svg.append('g').attr("width",bee_width-bee_margin.left-bee_margin.right).attr("height",bee_height-bee_margin.top-bee_margin.bottom)
                    .attr('transform', "translate("+bee_margin.left+","+bee_margin.top+")")

        var xScale = d3.scalePoint().domain(mod).range([0, bee_width-bee_margin.left-bee_margin.right]).padding(0.5);
        var xAxis=d3.axisBottom().scale(xScale)
        bee_svg.append("g").attr("transform", "translate(10," + (bee_height-100)+ ")").call(xAxis).style("font-size","11px").style("font-weight","bold")
        .selectAll("text")	
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-45)");        
        var yScale = d3.scaleLinear().domain(extent).range([bee_height-bee_margin.top-bee_margin.bottom, 0])
        var yAxis = d3.axisLeft().scale(yScale).ticks(5).tickFormat(d3.format(".1f")); 
        bee_svg.append("g").attr("transform", "translate(10, 0)").call(yAxis).style("font-size","11px").style("font-weight","bold")

        function make_x_gridlines() {		
            return d3.axisBottom(xScale)
                .ticks(model_list.length)
        }
        function make_y_gridlines() {		
            return d3.axisLeft(yScale)
                .ticks(5)
        }
        bee_svg.append("g")			
        .attr("class", "grid")
        .attr("transform", "translate(10," + (bee_height-100)+ ")")
            .call(make_x_gridlines()
            .tickSize(-(bee_height-bee_margin.top-bee_margin.bottom))
            .tickFormat("")
        ).style('stroke','lightgrey').style('stroke-opacity',0.2)  
        bee_svg.append("g")			
            .attr("class", "grid")
            .call(make_y_gridlines()
                .tickSize(-(bee_width-bee_margin.left-bee_margin.right))
                .tickFormat("")
            ).attr("transform", "translate(10, 0)")
            .style('stroke','lightgrey').style('stroke-opacity',0.2)


        var tooltip = d3.select("body")
        .append("div")
        .style("position", "absolute")
        .style("opacity", ".8")
        .style("visibility", "hidden")
        .style("color","white")
        .style("background-color", "black")
            .style("border-radius", "2px")
        .style("padding", "5px")
        .style("font-family","sans-serif")
        .style("font-size","12px")
        ;

        bee_svg.append('g').selectAll('dot').data(data).enter().append('circle')
            .attr('class','circw')
            .attr('id',function(d){return "cw-"+d.Model})
            .attr("r","7")
            .attr("cx",function(d){return 10+xScale(d.Model)})
            .attr("cy",function(d){return yScale(parseFloat(d.Score))})
            .attr("stroke","black")
            .attr("stroke-width",1)
            .attr("fill",function(d){if(d.Model==d.WModel){return "#FFDA00"} return "red"})
            .on('mouseover', function(d){
                var sco
                if(metric_selected=='WMProb'){sco='MProb'}
                else if(metric_selected=='WOOD'){sco='STS'}
                else if(metric_selected=='WSBias'){sco='Bias'}
                tooltip.html("<center><strong>"+sco+": "+d.Score+"</center>");
                return tooltip.style("visibility", "visible");
                }
            )
            .on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
            .on("mouseout", function(){return tooltip.style("visibility", "hidden");});

            bee_svg.append('g').selectAll('dot').data(data).enter().append('circle')
            .attr('class','circa')
            .attr('id',function(d){return "ca-"+d.Model})
            .attr("r","7")
            .attr("cx",function(d){return 10+xScale(d.Model)})
            .attr("cy",function(d){return yScale(parseFloat(d.Acc))})
            .attr("stroke","black")
            .attr("stroke-width",1)
            .attr("fill","#4472C4")
            .on('mouseover', function(d){
                tooltip.html("<center><strong>Accuracy: "+d.Acc+"</center>");
                return tooltip.style("visibility", "visible");
                }
            )
            .on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
            .on("mouseout", function(){return tooltip.style("visibility", "hidden");});

        for(i=0;i<mod.length-1;i++){
                var x1=d3.select("#ca-"+mod[i]).attr("cx")
                var y1=d3.select("#ca-"+mod[i]).attr("cy")
                var x2=d3.select("#ca-"+mod[i+1]).attr("cx")
                var y2=d3.select("#ca-"+mod[i+1]).attr("cy")
                bee_svg.append('line')
                .style("stroke", "#4472C4")
                .style("stroke-width", 3)
                .attr("x1", x1)
                .attr("y1", y1)
                .attr("x2", x2)
                .attr("y2", y2);         
        }        
        for(i=0;i<mod.length-1;i++){
            var x1=d3.select("#cw-"+mod[i]).attr("cx")
            var y1=d3.select("#cw-"+mod[i]).attr("cy")
            var x2=d3.select("#cw-"+mod[i+1]).attr("cx")
            var y2=d3.select("#cw-"+mod[i+1]).attr("cy")
            bee_svg.append('line')
            .style("stroke", "#FFDA00")
            .style("stroke-width", 3)
            .attr("x1", x1)
            .attr("y1", y1)
            .attr("x2", x2)
            .attr("y2", y2);
    } 
    var controls = d3.select(".righttop").append("label").attr("id", "controls").style("position","absolute").style("top",240).style("left",1542);
    controls.append("text").style("font-size","20px").text("Model Ranking").style('font-weight','bold')
    controls = d3.select(".righttop").append("label").attr("id", "controls").style("position","absolute").style("top",280).style("left",1492);
    controls.append("text").style("font-size","16px").text("Accuracy").style('font-weight','bold')
    controls = d3.select(".righttop").append("label").attr("id", "controls").style("position","absolute").style("top",280).style("left",1642);
    controls.append("text").style("font-size","16px").text(metric_selected).style('font-weight','bold')
    var m=[],wm=[]
    data.forEach(function(d){
        m.push(d.Model)
        wm.push(d.WModel)
    })
    for(i=1;i<=m.length;i++){
        controls = d3.select(".righttop").append("label").attr("id", "controls").style("position","absolute").style("top",320+20*(i-1)).style("left",1492);
        controls.append("text").style("font-size","11px").text(i+'. '+m[i-1])
        controls = d3.select(".righttop").append("label").attr("id", "controls").style("position","absolute").style("top",320+20*(i-1)).style("left",1642);
        controls.append("text").style("font-size","11px").text(i+'. '+wm[i-1])
    }
    });
}

function sun(fpath){
    d3.select("#beesun").remove()
    d3.select("#controls").remove()
    d3.csv(fpath,function(data) {
        bee_data=[]
        data.forEach(function(d){
            bee_data.push(Object.entries(d))
        })
        var tooltip = d3.select("body")
        .append("div")
        .style("position", "absolute")
        .style("opacity", ".8")
        .style("visibility", "hidden")
        .style("color","white")
        .style("background-color", "black")
            .style("border-radius", "2px")
        .style("padding", "5px")
        .style("font-family","sans-serif")
        .style("font-size","12px")
        ;
        var bee_width=+d3.select('.rightbottom').style('width').split('p')[0]
        var bee_height=+d3.select('.rightbottom').style('height').split('p')[0]
        var bee_margin = {top: 20, bottom: 20, left: 20, right:20}
        var bee_svg = d3.select('.rightbottom').append('svg').attr('width', bee_width).attr('height', bee_width).attr('id','beesun')
        .attr('transform', "translate(0,60)")
        bee_svg=bee_svg.append('g').attr("width",bee_width-bee_margin.left-bee_margin.right).attr("height",bee_height-bee_margin.top-bee_margin.bottom)
                    .attr('transform', "translate("+bee_margin.left+","+bee_margin.top+")")
        var controls = d3.select(".rightbottom").append("label").attr("id", "controls").style("position","absolute").style("top",600).style("left",1475);
        controls.append("text").style("font-size","16px").text('Select Model: ')
        var cb3=controls.append('select').attr("id", "modelsplit").style('width',130).style('position','relative').style('left',5).style('height',10)
        var xsplit=['Choose Model']
        var mod=model_list.split('\n')
        var splitcolor=["#ffffb3","#bebada","#80b1d3","#fdb462","#b3de69","#fccde5","#d9d9d9","#bc80bd","#ccebc5","#ffed6f"]
        for(i=0;i<mod.length;i++){
            xsplit.push(mod[i])
        }
        d3.select("#modelsplit")
        .selectAll('myOptions')
        .data(xsplit)
        .enter()
          .append('option')
        .text(function (d) { return d; })
        .attr("value", function (d) { return d; })
        cb3.on('change',function(){
            var choice=d3.select('#modelsplit').property("value")
            d3.selectAll('#beesun').remove()
            bee_svg = d3.select('.rightbottom').append('svg').attr('width', bee_width).attr('height', bee_width).attr('id','beesun')
            .attr('transform', "translate(0,60)")
            bee_svg=bee_svg.append('g').attr("width",bee_width-bee_margin.left-bee_margin.right).attr("height",bee_height-bee_margin.top-bee_margin.bottom)
                        .attr('transform', "translate("+bee_margin.left+","+bee_margin.top+")")        
        if(choice!='Choose Model'){
            var dictin = {};
            var dictout = {};
            data.forEach(function(d){
                if(d.Model==choice){
                    dictin[d.Split]=+d.Size
                    dictout[d.Split+'-C']=+d.Correct
                    dictout[d.Split+'-I']=+d.Incorrect
                }
            })
            var radius = bee_width/ 2 - 60
            var color = d3.scaleOrdinal()
            .domain(dictin)
            .range(splitcolor)   
            var pie = d3.pie()
                    .value(function(d) {return d.value; }).sort(null); 
            var data_ready = pie(d3.entries(dictin))
            var tw=(bee_width-40)/2
            bee_svg
            .selectAll('pie')
            .data(data_ready)
            .enter()
            .append('path')
            .attr('d', d3.arc()
              .innerRadius(50)         
              .outerRadius(radius)
            )
            .attr('fill', function(d){ return(color(d.data.key)) })
            .attr("stroke", "black")
            .style("stroke-width", "2px")
            .style("opacity", 0.7)
            .attr('transform', "translate("+tw+","+tw+")")
            .on('mouseover', function(d){d3.select(this).style('stroke-width','5px')
                tooltip.html("<center><strong>Split "+d.data.key+": </strong>"+d.data.value+"</center>");
                return tooltip.style("visibility", "visible");
                    }
            )
            .on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
            .on("mouseout", function(){d3.select(this).style('stroke-width','2px');return tooltip.style("visibility", "hidden");});
            
            var pie = d3.pie()
                    .value(function(d) {return d.value; }).sort(null); 
            var data_ready = pie(d3.entries(dictout))
            var tw=(bee_width-40)/2
            bee_svg
            .selectAll('pie')
            .data(data_ready)
            .enter()
            .append('path')
            .attr('d', d3.arc()
              .innerRadius(bee_width/ 2 - 60)         
              .outerRadius(bee_width/ 2 - 20)
            )
            .attr('fill', function(d){ var st=d.data.key;st=st.split('-')[1];if(st=='C'){return('#8dd3c7')}return '#fb8072' })
            .attr("stroke", "black")
            .style("stroke-width", "2px")
            .style("opacity", 0.7)
            .attr('transform', "translate("+tw+","+tw+")")
            .on('mouseover', function(d){
                d3.select(this).style('stroke-width','5px')
                var st=d.data.key;st=st.split('-');
                var htxt
                if(st[1]=='C'){htxt='Correct'}
                else{htxt='Incorrect'}
                tooltip.html("<center><strong>Split "+st[0]+"<br/>"+htxt+": </strong>"+d.data.value+"</center>");
                return tooltip.style("visibility", "visible");
                    }
            )
            .on("mousemove", function(){
                return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
            .on("mouseout", function(){d3.select(this).style('stroke-width','2px')
            return tooltip.style("visibility", "hidden");});
            console.log(dictin,dictout,choice)                        
            }
        })        
    });
}





        



 
 
