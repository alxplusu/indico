# This file is part of Indico.
# Copyright (C) 2002 - 2025 CERN
#
# Indico is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see the
# LICENSE file for more details.

import posixpath

from indico.core.config import config
from indico.core.db import db
from indico.core.storage.models import StoredFileMixin
from indico.util.fs import secure_filename
from indico.util.locators import locator_property
from indico.util.string import format_repr, strict_str


class PaperTemplate(StoredFileMixin, db.Model):
    __tablename__ = 'templates'
    __table_args__ = {'schema': 'event_paper_reviewing'}

    # StoredFileMixin settings
    add_file_date_column = False

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    event_id = db.Column(
        db.Integer,
        db.ForeignKey('events.events.id'),
        index=True,
        nullable=False
    )
    name = db.Column(
        db.String,
        nullable=False
    )
    description = db.Column(
        db.Text,
        nullable=False,
        default=''
    )

    event = db.relationship(
        'Event',
        lazy=True,
        backref=db.backref(
            'paper_templates',
            cascade='all, delete-orphan',
            lazy=True
        )
    )

    def __repr__(self):
        return format_repr(self, 'id', 'event_id', 'filename', content_type=None)

    @locator_property
    def locator(self):
        return dict(self.event.locator, template_id=self.id, filename=self.filename)

    def _build_storage_path(self):
        self.assign_id()
        path_segments = ['event', strict_str(self.event.id), 'paper_templates']
        filename = '{}_{}'.format(self.id, secure_filename(self.filename, 'file'))
        path = posixpath.join(*path_segments, filename)
        return config.ATTACHMENT_STORAGE, path
