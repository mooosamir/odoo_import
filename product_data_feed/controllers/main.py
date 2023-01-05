# Copyright © 2020 Garazd Creation (https://garazd.biz)
# @author: Yurii Razumovskyi (support@garazd.biz)
# @author: Iryna Razumovska (support@garazd.biz)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

import logging

from odoo.http import request
from werkzeug.exceptions import Forbidden, NotFound

from odoo import http, models

_logger = logging.getLogger(__name__)


class ProductFeed(http.Controller):

    def _validate_feed_request(self, feed_id, feed_name, **kwargs):
        """Check a feed request.

        :param string feed_id: a feed id
        :return: http response or True if everything is ok
        """
        if not (feed_id or feed_name):
            return NotFound()
        try:
            if feed_id:
                domain = [('id', '=', int(feed_id))]
            else:
                domain = [('filename', '=', str(feed_name))]
            feed = request.env['product.data.feed'].search(domain, limit=1)
        except ValueError:
            return NotFound()
        if not feed:
            return NotFound()

        # Check website
        if feed.website_ids and request.website not in feed.website_ids:
            return NotFound()

        # Check token
        if feed.use_token:
            access_token = kwargs.get('access_token')
            if not access_token or feed.access_token != access_token:
                return Forbidden()

        return feed

    def _get_mimetype(self, file_type):
        """Determinate a mimetype for a feed.

        :param string file_type: a feed file_type value
        :return: string or None
        """
        mimetype = None
        if file_type == 'csv':
            mimetype = 'text/csv;charset=utf-8'
        elif file_type == 'tsv':
            mimetype = 'text/tab-separated-values;charset=utf-8'
        return mimetype

    @http.route(['/product_data/<model("product.data.feed"):feed_id>/feed.csv',
                 '/product_data/<string:feed_name>.csv'],
                type='http',
                auth='public',
                website=True,
                multilang=False,
                sitemap=False)
    def product_data_feed(self, feed_id=None, feed_name=None, **kwargs):
        """Controller to return CSV/TSV product data feed."""

        feed = self._validate_feed_request(feed_id, feed_name, **kwargs)
        if not isinstance(feed, models.BaseModel):
            return feed

        mimetype = self._get_mimetype(feed.file_type)
        if not mimetype:
            return NotFound()

        try:
            content = feed.sudo().generate_data_file()
        except Exception as e:
            _logger.error("Error on generating of data feed: {}".format(e))
            return NotFound()

        return request.make_response(content, [('Content-Type', mimetype)])
