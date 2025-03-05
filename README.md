# **Trading Platform Application**  

This application uses a **Segment Tree** to efficiently retrieve statistical data with **O(log n)** time complexity.  

## **Prerequisites**  
Make sure you have **Docker** installed before running the application.  

## **Getting Started**  

### **Running the Application**  
To start the application:  
```sh
make run
```

To stop and remove the running containers:
```sh
make teardown
```

To run the tests:
```sh
make test
```

## Postman API Collection

To simplify API testing, a Postman collection is included.

### Importing the Collection
1. Open **Postman**.
2. Click **Import**.
3. Select the `postman/TradingPlatformAPI.postman_collection.json` file.

### Running Requests
- Make sure the application is running.
- Use the imported collection to test endpoints.


## How It Works

The application is built around a Segment Tree, which allows for fast statistical queries. Here's what it can do:

- Build the tree from an initial dataset.
- Add new data dynamically.
- Query the last 10^𝑘 elements and retrieve relevant stats.
- Remove old data when the size limit is reached.
- Resize automatically when needed to handle more data.

### Handling Memory Efficiently
- The tree starts with an initial capacity, so it doesn’t use unnecessary memory upfront.
- When more data arrives and exceeds this capacity, the tree resizes to fit the new entries.
- Since queries only need to handle a maximum window size (max_window_size), any data beyond that is removed.
- A buffer (capacity_buffer_factor) is included to store some extra data, reducing the need for frequent removals.
