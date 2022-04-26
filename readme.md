# Welcome to musicshare

Welcome to musicshare an api service in wich you can create your own playlists and share it with other.

You can even add songs ro other public shares or create your private ones.

## Login

First you should register in the app to be able to login, for it use the folowing endpoint:

```
mutation {
  register(
    email: "new_user@email.com",
    username: "new_user",
    password: "123456super",
  ) {
    success,
    errors,
    token,
    refreshToken
  }
}
```

You will recive a token an email user and a password, the token will expire in 20 minutes, but you can refresh your session using the refresh token endpoint.

```
mutation {
  refreshToken(
    token: "token"
  ) {
    success,
    errors,
    token,
    refreshToken
  }
}
```

You can also login ater a while in the login endpoint

```
mutation {
  tokenAuth(
      password: String!
      email: String
    ) {
        success,
        errors,
        token,
        refreshToken
    }
}
```

## Playlist

Once you are authenticated you can create your own playlist with the songs provided by the admins like this

```
mutation {playlistCreate(name:"playlistname", 
                         isPublic: true,
                         flag: "chill", 
                         loginsId:user,
                         songsId:song) {
                                playlist {
                                        name
                                        isPublic
                                        }
                                    }
                                }
```
You can also see the public playlists using this endpoint

```
query {playlists {results {
                            name
                        }    
                    }
                }
```
Or retrive one of your own

```
query {playlist(name: "name") {
                            results {
                                name
                            }
            }
        }
```

## Admin

If you are an admin you can also create, edit or delete the songs, artists, or albums of our database in a similar way.


### Use

To use this API on your server, you need to have a Linux distro and docker-compose installed. Use this command on your terminal to build and run the app

```
docker-compose build
```

and use this command to run the server

```
docker-compose up
```

To test the app use this command

```
docker-compose run django python3 manage.py test
```
