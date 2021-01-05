FROM golang:rc-alpine

COPY . /src
ENV GO111MODULE=on
RUN cd /src/cmd/go && go build -mod=vendor -o /usr/bin/go

EXPOSE 8067

CMD ["/usr/bin/go", "--data=/data"]


