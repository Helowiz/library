DROP TABLE IF EXISTS Edition;
DROP TABLE IF EXISTS Wrote;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Saga;
DROP TABLE IF EXISTS Publisher;
DROP TABLE IF EXISTS Authors;

CREATE TABLE Authors(
   idAuthor SERIAL,
   NameAuthor VARCHAR(255) NOT NULL,
   PRIMARY KEY(idAuthor)
);

CREATE TABLE Publisher(
   idPublisher INT,
   NamePublisher VARCHAR(255) NOT NULL,
   LangageEdition VARCHAR(50) NOT NULL,
   PRIMARY KEY(idPublisher),
   UNIQUE(NamePublisher)
);

CREATE TABLE Saga(
   idSaga INT,
   NameSaga VARCHAR(255) NOT NULL,
   NumberOfVolumes INT NOT NULL,
   PRIMARY KEY(idSaga),
   UNIQUE(NameSaga)
);

CREATE TABLE Books(
   ISBN BIGINT,
   Title VARCHAR(255) NOT NULL,
   Pages INT NOT NULL,
   Summery TEXT NOT NULL,
   idSaga INT,
   DateAdded date DEFAULT NOW(),
   PRIMARY KEY(ISBN),
   UNIQUE(Title),
   FOREIGN KEY(idSaga) REFERENCES Saga(idSaga)
);

CREATE TABLE Wrote(
   ISBN INT,
   idAuthor INT,
   PRIMARY KEY(ISBN, idAuthor),
   FOREIGN KEY(ISBN) REFERENCES Books(ISBN),
   FOREIGN KEY(idAuthor) REFERENCES Authors(idAuthor)
);

CREATE TABLE Edition(
   ISBN INT,
   idPublisher INT,
   YearEdition DATE NOT NULL,
   PRIMARY KEY(ISBN, idPublisher),
   FOREIGN KEY(ISBN) REFERENCES Books(ISBN),
   FOREIGN KEY(idPublisher) REFERENCES Publisher(idPublisher)
);
