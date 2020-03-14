import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Index from '@/components/Index'
import search from '@/components/search'
import product from '@/components/product'

Vue.use(Router)

export default new Router({
  // mode: 'history',  //去掉url中的#
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    {
      path: '/HelloWorld',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/search',
      name: 'search',
      component: search
    },
    {
      path: '/product',
      name: 'product',
      component: product
    }
    
  ]
})
