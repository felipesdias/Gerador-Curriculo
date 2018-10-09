
const routes = [
  {
    path: '*',
    component: () => import('layouts/GeradorPDF.vue'),
  }
]

export default routes
