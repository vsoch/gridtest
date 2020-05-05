// register the grid and model components

Vue.component("modal", {
    template: "#modal-template"
});

Vue.component('grid-tests', {
  template: '#grid-template',
  props: {
    heroes: Array,
    columns: Array,
    filterKey: String,
    tests: Object,
    showModal: false,
    mouseover: { type: Function },
  },
  data: function () {
    var sortOrders = {}
    this.columns.forEach(function (key) {
      sortOrders[key] = 1
    })
    return {
      sortKey: '',
      sortOrders: sortOrders
    }
  },
  computed: {
    filteredHeroes: function () {
      var sortKey = this.sortKey
      var filterKey = this.filterKey && this.filterKey.toLowerCase()
      var order = this.sortOrders[sortKey] || 1
      var heroes = this.heroes
      if (filterKey) {
        heroes = heroes.filter(function (row) {
          return Object.keys(row).some(function (key) {
            return String(row[key]).toLowerCase().indexOf(filterKey) > -1
          })
        })
      }
      if (sortKey) {
        heroes = heroes.slice().sort(function (a, b) {
          a = a[sortKey]
          b = b[sortKey]
          return (a === b ? 0 : a > b ? 1 : -1) * order
        })
      }
      return heroes
    }
  },
  filters: {
    capitalize: function (str) {
      return str.charAt(0).toUpperCase() + str.slice(1)
    }
  },
  methods: {
    sortBy: function (key) {
      this.sortKey = key
      this.sortOrders[key] = this.sortOrders[key] * -1
    }
  }
})

var demo = new Vue({
  el: '#main',
  created: function() {
      this.fetchData();
  },
  methods: {

    activate: function(name) {
        if (this.lookup.hasOwnProperty(name)) {
           this.gridData = this.lookup[name]
        }
    },

    mouseover: function(name) {
      var metrics = ""
      $.each(this.tests[name]['metrics'], function(i,e){
          metrics += (i + ": " + e + "<br>")
      })

      // Parse the output depending on what is available
      var body = ("<strong>out</strong>: " + this.tests[name]['out'] + "<br>" +
                  "<strong>err</strong>: " + this.tests[name]["err"] + "<br>" +
                  "<strong>metrics</strong>: " + "<br>" + metrics + "<br>"+
                  "<strong>raises</strong>: " + this.tests[name]['raises'] + "<br>" +
                  "<strong>success</strong>: " + this.tests[name]['success'] + "<br>" +
                  "<strong>result</strong>: " + this.tests[name]['result'] + "<br>");

      this.modalHeader = name;
      this.modalBody = body
      this.showModal = true;
    },

    fetchData: function () {

      var self = this;
      self.tests = Object()
      self.sidebar = Object()

      var xhr = new XMLHttpRequest()
      xhr.open('GET', "results.json")
      xhr.onload = function () {
        raw = JSON.parse(xhr.responseText)

        $.each(raw, function(i,e){

          // Truncate result
          var slug = e['result']
          if (slug.length > 80){
            slug = slug.slice(0,79);
          }
          self.tests[e['name']] = e

          // We haven't added the function to the lookup yet
          if (! self.lookup.hasOwnProperty(e['function'])) {
            self.lookup[e['function']] = Array()
          }

          // If not yet added to sidebar lookup
          if (! self.sidebar.hasOwnProperty(e['function'])) {
            self.sidebar[e['function']] = {name: e['function'], success: e['success']}
          }
          // If we have a failure, entire set is considered failure 
          if (e['success'] == "false") {
            self.sidebar[e['function']]['success'] = e['success']
          }
          self.lookup[e['function']].push({module: e['module'],
                                           name: e['name'], 
                                           success: e['success'],
                                           params: e['params']['args'],
                                           raises: e['raises'],
                                           result: slug})
          })
                
          // Set the table to be the first in the sidebar 
          if (Object.keys(self.lookup).length > 0) {
            self.gridData = self.lookup[Object.keys(self.lookup)[0]]
            console.log(self.gridData);
          }
       }
       xhr.send()
    }
  },
  data: {
    showModal: false,
    modalBody: "",
    modalHeader: "",
    modalFooter: "",

    sidebar: Object(),
    lookup: Object(),
    searchQuery: '',
    gridColumns: ['module', 'name', 'success', 'args', 'raises', 'result'],
    gridData: Array(),
  }
})
