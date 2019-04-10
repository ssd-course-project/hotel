/*
 * Copyright (C) 2015 Jose F. Maldonado
 * This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. 
 * If a copy of the MPL was not distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */

// Verify if the namespace is not already defined.
if(typeof SaVaGe !== 'object') SaVaGe = {};

/**
 * Creates a SVG element representing a bheckbox.
 * 
 * The parameter must be an object with the following attributes:
 * 'container' (a selector of the element where the element must be appended),
 * 'size' (the widht and height, in pixels, of the checkbox, by default 25),
 * 'value' (a number between 0 and 2, indicating the initial state of the checkbox),
 * 'border' (an object with the numerical attributes 'width' and 'radius' indicating the width of the checkbox's border and the radius of his corners,
 * 'tristate' (a boolean indicating if the chechbox must have three states [unchecked, checked and cancelled], instead of only two [checked and unchecked]),
 * 'marks' (an object with the attributes 'unchecked', 'checked' and 'cancelled', which indicates which kind of mark must be used for represent each state, their possible values are 'empty', 'tick', 'cross' and 'fill'),
 * 'colors' (an object with the attributes 'border', 'back', 'tick', 'cross' and 'fill' indicating the different colors used in the checkbox),
 * 
 * The object returned by this function contains the methods:
 * 'svg', and instance of the SVG object created with D3.js,
 * 'getValue()', for get the current state of the checkbox (a number between 0 and 2),
 * 'serValue(newVal)', for change the state of the checkbox and
 * 'remove()', for remove the element from the document.
 * 
 * @param {object} params An collection of values for customize the element.
 * @returns {object} An object with methods for manipulate the element.
 */
SaVaGe.CheckBox = function(params) {
    // Verify parameters.
    if(typeof params !== 'object') params = {};
    if(typeof params.container !== 'string') params.container = "body";
    if(typeof params.size !== 'number') params.size = 23;
    if(typeof params.value !== 'number') params.value = 0;
    if(typeof params.border !== 'object') params.border = {};
    if(typeof params.duration !== 'number') params.duration = 250;
    if(typeof params.border.radius !== 'number') params.border.radius = 0;
    if(typeof params.border.width !== 'number') params.border.width = 0;
    if(typeof params.tristate !== 'boolean') params.tristate = false;
    if(typeof params.marks !== 'object') params.marks = {};
    if(typeof params.marks.unchecked !== "string") params.marks.unchecked = "empty";
    if(typeof params.marks.checked !== "string") params.marks.checked = "tick";
    if(typeof params.marks.cancelled !== "string") params.marks.cancelled = "cross";
    if(typeof params.colors !== 'object') params.colors = {};
    if(typeof params.colors.back === "undefined") params.colors.back = "none";
    if(typeof params.colors.border === "undefined") params.colors.border = "none";
    if(typeof params.colors.cross === "undefined") params.colors.cross = "none";
    if(typeof params.colors.tickOn === "undefined") params.colors.tickOn = "#fff";
    if(typeof params.colors.tickOff === "undefined") params.colors.tickOff = "#c0c0c0";
    if(typeof params.colors.fillOn === "undefined") params.colors.fillOn = "#4eb7a8";
    if(typeof params.colors.fillOff === "undefined") params.colors.fillOff = "#e5e5e5";
    
    // Define internal variables.
    var state = 0;
    
    // Create widget.
    var svg = d3.select(params.container).append("svg")
            .attr("width", params.size + params.border.width*2)
            .attr("height", params.size + params.border.width*2)
            .style("cursor", "pointer");
    var circle = svg.append("circle")
            .attr("x", params.border.width)
            .attr("y", params.border.width)
            .attr("cx", params.size/2)
            .attr("cy", params.size/2)
            .style("fill", params.colors.fillOff)
            .style("stroke", params.colors.border)
            .style("stroke-width", params.border.width)
            .attr("r", params.size/2);
    var mark = null;

    // Define internal functions.
    var setState = function(newState) {
        // Set new state.
        state = params.tristate? newState%3 : newState%2;
        
        // Remove old mark.
        if(mark !== null) mark.remove();
        
        // Find the symbol of the new mark.
        var symbol = null;
        if(state === 0) symbol = params.marks.unchecked;
        else if(state === 1) symbol = params.marks.checked;
        else symbol = params.marks.cancelled; // state = 2
        
        // Add new mark.
        if(symbol === "empty") {
            // mark = null;
            var width = 2;

            var lineFunction = d3.svg.line().x(function(d) { return d.x; }).y(function(d) { return d.y; }).interpolate("linear");
            var lineData = [
                { "x": params.size/2 + params.size/4, "y": params.size/3},
                { "x": params.size/3 + params.size/12, "y": params.size/2 + params.size/6},
                { "x": params.size/4, "y": params.size/2}
                ];
            mark = svg.append("path")
                .attr("d", lineFunction(lineData))
                .attr("stroke", params.colors.tickOff)
                .attr("stroke-width", width)
                .attr("fill", "none");
            circle.transition().duration(params.duration).style("fill", params.colors.fillOff);

        } else if(symbol === "tick") {
            // Draw two lines.
            var width = 2;

            var lineFunction = d3.svg.line().x(function(d) { return d.x; }).y(function(d) { return d.y; }).interpolate("linear");
            var lineData = [
                { "x": params.size/2 + params.size/4, "y": params.size/3},
                { "x": params.size/3 + params.size/12, "y": params.size/2 + params.size/6},
                { "x": params.size/4, "y": params.size/2}
                ];
            mark = svg.append("path")
                .attr("d", lineFunction(lineData))
                .attr("stroke", params.colors.tickOn)
                .attr("stroke-width", width)
                .attr("fill", "none");
            circle.transition().duration(params.duration).style("fill", params.colors.fillOn);

        } else if(symbol === "cross") {
            // Draw two crossed lines.
            var width = parseInt(params.size/5, 10);
            if(width < 2) width = 2;
            
            mark = svg.append("g");
            mark.append("line")
                .attr("x1", params.border.width + width/2)
                .attr("y1", params.border.width + width/2)
                .attr("x2", params.border.width + params.size - width/2)
                .attr("y2", params.border.width + params.size - width/2)
                .style("stroke", params.colors.cross)
                .style("stroke-width", width);
            mark.append("line")
                .attr("x1", params.border.width + params.size - width/2)
                .attr("y1", params.border.width + width/2)
                .attr("x2", params.border.width + width/2)
                .attr("y2", params.border.width + params.size - width/2)
                .style("stroke", params.colors.cross)
                .style("stroke-width", width);
        } else if(symbol === "fill") {
            // Draw an smaller rectable.
            var space = parseInt(params.size/10, 10);
            if(space < 1) space = 1;
            
            mark = svg.append("circle")
                .attr("x", params.border.width + space)
                .attr("y", params.border.width + space)
                .attr("cx", params.size/2)
                .attr("cy", params.size/2)
                .style("fill", params.colors.fill)
                .attr("r", params.size/2 - space*2);
        }
    };
    
    // Set initial state.
    setState(params.value);
    
    // Define result's object.
    var res = {
        'svg' : svg,
        'getValue': function() { return state; },
        'setValue': setState,
        'remove': function() { svg.remove(); }
    };

    // Define click listener.
    svg.on('click', function(data, index){
        setState(state + 1);
        if(typeof params.onChange === 'function') params.onChange(res);
    });    
    
    return res;
};
