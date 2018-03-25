// sample names - api endpoint 
var sampleNamesUrl = '/names'

Plotly.d3.json(sampleNamesUrl, function(error, sampleNames) {
    if (error) {
        return console.warn(error);
    };

    sampleNames.forEach( function(name) {
        Plotly.d3
        .select('#selDataset')
        .append('option')
        .attr('value', name)
        .attr('class', 'dropDownItem')
        .text(name)
    });
});


// capture changes - dropdown selection

function optionChanged(sample) {
    // sample blank? default to BB_940
    sample = (sample === '' ? 'BB_940': sample)

    // url def
    var sampleURL = `/sample/${sample}`;
    var otuURL = '/otu';
    var metadataURL = `/meta/${sample}`;
    var wfreqURL = `/wfreq/${sample}`;

    // sample endpoint - api call
    Plotly.d3.json(sampleURL, function(error, sampleResponse) {
        if (error) {
                console.warn(error);
            };
            
        var Values = sampleResponse.sample_values;
        var otuIDs = sampleResponse.otu_ids;

        
        // otu endpoint - api call
        Plotly.d3.json(otuURL, function(error, otuResponse) {
            if (error) {
                console.warn(error);
            }
    
            var Descriptions = [];
            IDs.forEach( function(data) {
                Descriptions.push(otuResponse[data]);
            })
            
            Plotly.d3.json(metadataURL, function(error, metaResponse) {
                if (error) {    
                    console.warn(error)
                }

                var age, bbType, ethnicity, gender, location, sampleID;

                age = metaResponse.AGE;
                bbType = metaResponse.BBTYPE;
                ethnicity = metaResponse.ETHNICITY;
                gender = metaResponse.GENDER;
                location = metaResponse.LOCATION;
                sampleID = metaResponse.SAMPLEID;

                Plotly.d3.json(wfreqURL, function(error, wfreqResponse){
                    if (error) {
                        console.warn(error)
                    }                      

                        // update sample meta
                        Plotly.d3.select('#age').text(`AGE: ${age}`)
                        Plotly.d3.select('#bbType').text(`BBTYPE: ${bbType}`)
                        Plotly.d3.select('#ethnicity').text(`ETHNICITY: ${ethnicity}`)
                        Plotly.d3.select('#gender').text(`GENDER: ${gender}`)
                        Plotly.d3.select('#location').text(`LOCATION: ${location}`)
                        Plotly.d3.select('#sampleID').text(`SAMPLEID: ${sampleID}`)

optionChanged("");