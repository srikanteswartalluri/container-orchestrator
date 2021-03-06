db.master.insert( {
    contact: "srikanth",
    address: "Hyderabad"
})
db.createUser(
    {
        user: "co",
        pwd: "co123",
        roles: [
            {
                role: "readWrite",
                db: "co_db"
            }
        ]
    }
)