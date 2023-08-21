conn = Mongo();
db = conn.getDB('library');

db.test.insertOne({
  _id: ObjectId('633184f42ec069ab607b0b5b'),
  full_name: 'Librarian',
});
// db.accounts.createIndex(
//   {full_name: 1},
//   {unique: true},
// );
