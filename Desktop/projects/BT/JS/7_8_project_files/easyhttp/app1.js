const http = new easyHTTP;

// // Get Posts
// http.get('https://jsonplaceholder.typicode.com/posts', function(err, posts) {
//   if(err) {
//     console.log(err);
//   } else {
//     console.log(posts);
//   }
// });



// // Get single post

// http.get('https://jsonplaceholder.typicode.com/posts/4', function(err, post){
//   if(err){
//     console.log(err);
//   } else {
//     console.log(post);
//   }
// });


//  Create Data

const data = {
  title: 'Custom Post',
  body: 'This is a custom post'
};

// Create Post

// http.post('https://jsonplaceholder.typicode.com/posts', data, function(err,post){
//   if(err){
//     console.log(err);
//   } else {
//     console.log(post);
//   }
// });

//Upadate Post

// http.put('https://jsonplaceholder.typicode.com/posts/5', data, function(err, post){
//   if(err) {
//     console.log(err);
//   } else {
//     console.log(post);
//   }
// });

// Delete post

http.delete('https://jsonplaceholder.typicode.com/posts/1', data, function(err, response){
  if(err) {
    console.log(err);
  } else {
    console.log(response);
  }
});