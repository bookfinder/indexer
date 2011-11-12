CREATE TABLE libraries (
   id                   bigserial NOT NULL,
   name                 character varying(255) UNIQUE NOT NULL,
   phone                character varying(25) NOT NULL,
   address              character varying(255) NOT NULL,
   monday               character varying(255) NOT NULL,
   tuesday              character varying(255) NOT NULL,
   wednesday            character varying(255) NOT NULL,
   thursday             character varying(255) NOT NULL,
   friday               character varying(255) NOT NULL,
   saturday             character varying(255) NOT NULL,
   sunday               character varying(255) NOT NULL,
   lat                  double precision,
   lon                  double precision,

   CONSTRAINT           libraries_pk PRIMARY KEY (id)
);


CREATE TABLE editors (
   id                   bigserial NOT NULL,
   name                 character varying(255) UNIQUE NOT NULL,

   CONSTRAINT           editors_pk PRIMARY KEY (id)
);


CREATE TABLE authors (
   id                   bigserial NOT NULL,
   author               character varying(255) UNIQUE NOT NULL,
   author_tsv           tsvector,

   CONSTRAINT           authors_pk PRIMARY KEY (id)
);

CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE ON authors
   FOR EACH ROW EXECUTE PROCEDURE tsvector_update_trigger(author_tsv, 'pg_catalog.english', author);

CREATE INDEX authors_author_tsv  ON authors USING gin(author_tsv);


CREATE TABLE documents (
   id                   bigserial NOT NULL,
   library_id           bigint NOT NULL,
   isbn                 character varying(255) UNIQUE NOT NULL,
   editor_id            bigint NULL,
   doctype              character varying(255) NULL,
   type                 character varying(255) NULL,
   author_id            bigint NULL,
   title                character varying(255) NOT NULL,
   title_tsv            tsvector,
   subject              character varying(255) NOT NULL,
   subject_tsv          tsvector,
   years                character varying(255) NOT NULL,
   price_amazone        real NULL,
   google_book          boolean default false,

   CONSTRAINT           documents_pk PRIMARY KEY (id),

   CONSTRAINT           documents_library_id_fk
                           FOREIGN KEY (library_id)
                           REFERENCES libraries(id),

   CONSTRAINT           documents_editor_id_fk
                           FOREIGN KEY (editor_id)
                           REFERENCES editors(id),

   CONSTRAINT           documents_author_id_fk
                           FOREIGN KEY (author_id)
                           REFERENCES authors(id)
);

CREATE INDEX documents_doctype_idx ON documents(doctype);

CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE ON documents
   FOR EACH ROW EXECUTE PROCEDURE tsvector_update_trigger(title_tsv, 'pg_catalog.english', title);

CREATE TRIGGER tsvectorupdate2 BEFORE INSERT OR UPDATE ON documents
   FOR EACH ROW EXECUTE PROCEDURE tsvector_update_trigger(subject_tsv, 'pg_catalog.english', subject);

CREATE INDEX documents_title_tsv   ON documents USING gin(title_tsv);
CREATE INDEX documents_subject_tsv ON documents USING gin(subject_tsv);


CREATE TABLE libraries_documents (
   library_id           bigint NOT NULL,
   document_id          bigint NOT NULL,

   CONSTRAINT           libraries_documents_pk PRIMARY KEY (library_id, document_id),

   CONSTRAINT           librairies_documents_library_id_fk
                           FOREIGN KEY (library_id)
                           REFERENCES libraries(id),

   CONSTRAINT           librairies_documents_document_id_fk
                           FOREIGN KEY (document_id)
                           REFERENCES documents(id)
);


