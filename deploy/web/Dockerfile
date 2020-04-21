FROM node:9.11.1-alpine

# install simple http server for serving static content
RUN npm install -g http-server
WORKDIR .

# copy both 'package.json' and 'package-lock.json' (if available)
COPY web/package*.json ./

# install project dependencies

# https://github.com/nodejs/docker-node/issues/384
# https://github.com/WordPress/gutenberg/issues/9474
RUN apk --no-cache add --virtual native-deps \
  g++ gcc libgcc libstdc++ linux-headers make python && \
  rm -rf node_modules &&\
  npm install --quiet node-gyp -g &&\
  npm install --quiet && \
  apk del native-deps

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY web/ .

# build app for production with minification
RUN npm run build
EXPOSE 80
CMD http-server dist --port 80
