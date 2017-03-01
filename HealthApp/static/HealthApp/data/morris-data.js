$(function() {

    Morris.Area({
        element: 'morris-area-chart',
        data: [{
            year: '2010 Q2',
            height: 70,
            weight: 178
        }, {
            year: '2011 Q2',
            height: 71,
            weight: 175
        }, {
            year: '2012 Q2',
            height: 71,
            weight: 169
        }, {
            year: '2013 Q2',
            height: 72,
            weight: 192
        }, {
            period: '2014 Q2',
            height: 72,
            weight: 191
        }, {
            period: '2015 Q2',
            height: 73,
            weight: 179
        }, {
            period: '2016 Q2',
            height: 75,
            weight: 176
        }, {
            period: '2017 Q2',
            height: 76,
            weight: 171
        }],
        xkey: 'period',
        ykeys: ['height', 'weight'],
        labels: ['Height', 'Weight'],
        pointSize: 2,
        hideHover: 'auto',
        resize: true
    });

    Morris.Donut({
        element: 'morris-donut-chart',
        data: [{
            label: "Download Sales",
            value: 12
        }, {
            label: "In-Store Sales",
            value: 30
        }, {
            label: "Mail-Order Sales",
            value: 20
        }],
        resize: true
    });

    Morris.Bar({
        element: 'morris-bar-chart',
        data: [{
            y: '2006',
            a: 100,
            b: 90
        }, {
            y: '2007',
            a: 75,
            b: 65
        }, {
            y: '2008',
            a: 50,
            b: 40
        }, {
            y: '2009',
            a: 75,
            b: 65
        }, {
            y: '2010',
            a: 50,
            b: 40
        }, {
            y: '2011',
            a: 75,
            b: 65
        }, {
            y: '2012',
            a: 100,
            b: 90
        }],
        xkey: 'y',
        ykeys: ['a', 'b'],
        labels: ['Series A', 'Series B'],
        hideHover: 'auto',
        resize: true
    });

});
