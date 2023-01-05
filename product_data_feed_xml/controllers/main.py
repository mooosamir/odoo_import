import logging

from werkzeug.exceptions import NotFound

from odoo import http, models
from odoo.http import request
from odoo.addons.product_data_feed.controllers.main import ProductFeed

_logger = logging.getLogger(__name__)


class ProductFeedXml(ProductFeed):

    def _get_mimetype(self, file_type):
        mimetype = super(ProductFeedXml, self)._get_mimetype(file_type)
        if file_type == 'xml':
            mimetype = 'application/xml;charset=utf-8'
        return mimetype

    @http.route(['/product_data/<model("product.data.feed"):feed_id>/feed.xml',
                 '/product_data/<string:feed_name>.xml'],
                type='http',
                auth='public',
                website=True,
                multilang=False,
                sitemap=False)
    def product_data_feed_xml(self, feed_id=None, feed_name=None, **kwargs):
        """Controller to return XML product data feed."""

        feed = self._validate_feed_request(feed_id, feed_name, **kwargs)
        if not isinstance(feed, models.BaseModel):
            return feed

        mimetype = self._get_mimetype(feed.file_type)
        if not mimetype:
            return NotFound()

        try:
            content = feed.sudo().generate_data_file_xml()
        except Exception as e:
            _logger.error("Error on generating of data feed: {}".format(e))
            return NotFound()

        response = request.make_response(content, [('Content-Type', mimetype)])
        return response
