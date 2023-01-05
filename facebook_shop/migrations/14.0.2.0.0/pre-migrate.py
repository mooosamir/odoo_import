def migrate(cr, version):
    # Select Facebook feed recipients
    cr.execute("SELECT id FROM product_data_feed_recipient "
               "WHERE name='Facebook Catalog'")
    recipient_ids = cr.fetchall()
    # Select Facebook feeds
    cr.execute("SELECT id FROM product_data_feed "
               "WHERE recipient_id in %s",
               tuple(recipient_ids))
    feed_ids = cr.fetchall()
    # Select Facebook feed columns 'Availability'
    cr.execute("SELECT id FROM product_data_feed_column "
               "WHERE type='special' AND name='availability' "
               "AND feed_id IN %s",
               [tuple(rec_id[0] for rec_id in feed_ids)])
    column_ids = cr.fetchall()
    # Update columns 'Availability'
    if column_ids:
        cr.execute(
            "UPDATE product_data_feed_column "
            "SET special_type='availability', "
            "special_avail_in='in stock', "
            "special_avail_out='out of stock', "
            "special_avail_order='available for order' "
            "WHERE id in %s",
            [tuple(rec_id[0] for rec_id in column_ids)])

    # Select Facebook feed columns 'Link'
    cr.execute("SELECT id FROM product_data_feed_column "
               "WHERE type='special' AND name='link' "
               "AND feed_id IN %s",
               [tuple(rec_id[0] for rec_id in feed_ids)])
    column_ids = cr.fetchall()
    # Update columns 'Link'
    if column_ids:
        cr.execute(
            "UPDATE product_data_feed_column "
            "SET special_type='link' WHERE id in %s",
            [tuple(rec_id[0] for rec_id in column_ids)])

    # Select Facebook feed columns 'Image Link'
    cr.execute("SELECT id FROM product_data_feed_column "
               "WHERE type='special' AND name='image_link' "
               "AND feed_id IN %s",
               [tuple(rec_id[0] for rec_id in feed_ids)])
    column_ids = cr.fetchall()
    # Update columns 'Image Link'
    if column_ids:
        cr.execute(
            "UPDATE product_data_feed_column "
            "SET special_type='image_link' WHERE id in %s",
            [tuple(rec_id[0] for rec_id in column_ids)])
