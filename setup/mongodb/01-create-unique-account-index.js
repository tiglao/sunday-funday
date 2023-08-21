conn = Mongo();
db = conn.getDB('sunday-funday');

// db.accounts.insertOne({
//   _id: ObjectId('633184f42ec069ab607b0b5b'),
//   email: 'librarian@example.com',
//   password: '$2b$12$gqB.kZtNIbyKcYxStjtVTenCwLcqmUSFN/Yda2rP1znKlTHX6wukq',
//   full_name: 'Librarian',
//   roles: [
//       'patron',
//       'librarian'
//   ]
// });
// db.accounts.insertOne({
//   _id: ObjectId('633185412ec069ab607b0b5c'),
//   email: 'patron@example.com',
//   password: '$2b$12$BnCFBYWNZI1dpQ3djPS5DuWszH3nc2v6nYPcz8OZpr6LPZSysrJty',
//   full_name: 'Patron',
//   roles: [
//       'patron'
//   ]
// });
// this is all that's needed. above are examples
db.accounts.createIndex(
  {email: 1},
  {unique: true},
);
