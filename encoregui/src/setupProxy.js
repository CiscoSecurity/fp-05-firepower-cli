const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {

  app.use(
    '/api/loadconfig/',
    createProxyMiddleware({
      target: 'http://127.0.0.1:8282',
      changeOrigin: true,
    })
  );

  app.use(
    '/api/',
    createProxyMiddleware({
      target: 'http://127.0.0.1:8282',
      changeOrigin: true,
    })
  );

  app.use(
    '/api/uploadfile/',
    createProxyMiddleware({
      target: 'http://127.0.0.1:8282',
      changeOrigin: true,
    })
  );

  app.use(
    '/api/modifyfile/',
    createProxyMiddleware({
      target: 'http://127.0.0.1:8282',
      changeOrigin: true,
    })
  );
}
