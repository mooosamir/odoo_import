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
    # Select Facebook feed columns 'price'
    if feed_ids:
        # Update columns 'price'
        cr.execute(
            "UPDATE product_data_feed "
            "SET currency_position='after' "
            "WHERE id in %s",
            [tuple(rec_id[0] for rec_id in feed_ids)])
        # Select columns 'price'
        cr.execute("SELECT id FROM product_data_feed_column "
                   "WHERE type='field' AND name='price' "
                   "AND feed_id IN %s",
                   [tuple(rec_id[0] for rec_id in feed_ids)])
        column_ids = cr.fetchall()
        # Update columns 'price'
        if column_ids:
            cr.execute(
                "UPDATE product_data_feed_column "
                "SET type='special',"
                "special_type='price' "
                "WHERE id in %s",
                [tuple(rec_id[0] for rec_id in column_ids)])
