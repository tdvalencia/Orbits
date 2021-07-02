
const api_url = 'http://127.0.0.1:5000/watermelon'

const testData = {
   "NUM_BODIES": 3,
   "NUM_STEPS": 378,
   "COLORS": ["orange","peru","lightseagreen"],
   "MASSES": [1.989e+30,3.3011e+23,5.972e+24],
   "NAMES": ["sun","mercury","earth"],
   "DIST": [0.0, -46000000000.0, -147095000000.0],
   "VEL": [0.0, -58980.0, -30300.0],
   "RADII": [695700000.0, 2439700.0, 6371000.0]
}

function getInput() {
   var form = document.getElementById('form')
   var jsonData = {}

   for (var x = 0; x < form.elements.length-1; x++) {
      var id = form.elements[x].id
      var val = form.elements[x].value
      jsonData[id] = val
   }

   return jsonData
}

function postApi(url, input) {
	var req = new XMLHttpRequest()
	req.open('POST', url)
	req.setRequestHeader('Content-Type', 'application/json;charset=UTF-8')
   req.onreadystatechange = function () {
      if (req.readyState == 4 && req.status == 200) {
         var json = JSON.parse(req.responseText)
         localStorage.setItem('json', JSON.stringify(json))
      }
   }
   req.send(JSON.stringify(input))
}

function graph() {
   console.log(JSON.parse(localStorage.getItem('json')))
}

document.getElementById('simulate').onclick = function() {
   postApi(api_url, testData)
   graph()
}