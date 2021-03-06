/*
 * Copyright 2011-2020 GatlingCorp (https://gatling.io)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *  http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package computerdatabase

import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._

class BasicSimulation extends Simulation {

  val httpProtocol = http
    .baseUrl("http://computer-database.gatling.io") // Here is the root for all relative URLs
    .acceptHeader("text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8") // Here are the common headers
    .doNotTrackHeader("1")
    .acceptLanguageHeader("en-US,en;q=0.5")
    .acceptEncodingHeader("gzip, deflate")
    .userAgentHeader("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20100101 Firefox/16.0")

  val scn = scenario("Scenario Name") // A scenario is a chain of requests and pauses
    .exec(
      http("request_1")
        .get("/")
    )
    .pause(7) // Note that Gatling has recorded real time pauses
    .exec(
      http("request_2")
        .get("/computers?f=macbook")
    )
    .pause(2)
    .exec(
      http("request_3")
        .get("/computers/6")
    )
    .pause(3)
    .exec(
      http("request_4")
        .get("/")
    )
    .pause(2)
    .exec(
      http("request_5")
        .get("/computers?p=1")
    )
    .pause(670 milliseconds)
    .exec(
      http("request_6")
        .get("/computers?p=2")
    )
    .pause(629 milliseconds)
    .exec(
      http("request_7")
        .get("/computers?p=3")
    )
    .pause(734 milliseconds)
    .exec(
      http("request_8")
        .get("/computers?p=4")
    )
    .pause(5)
    .exec(
      http("request_9")
        .get("/computers/new")
    )
    .pause(1)
    .exec(
      http("request_10") // Here's an example of a POST request
        .post("/computers")
        .formParam("name", "Beautiful Computer") // Note the triple double quotes: used in Scala for protecting a whole chain of characters (no need for backslash)
        .formParam("introduced", "2012-05-30")
        .formParam("discontinued", "")
        .formParam("company", "37")
    )
    .pause(1)
    .exec(
      http("request_11") // Here's an example of a POST request
        .post("/reader")
        .formParam("email", "johndoe@gmail.com") 
        .formParam("lname", "john")
        .formParam("fname", "doe")
        .formParam("libaccountno", "jd123456")
        .formParam("membershipexp", "2022-12-12")
    )
    .pause(1)
    .exec(
      http("request_12") // Here's an example of a GET request
        .get("/reader/12")
    )
    .pause(1)
    .exec(
      http("request_13") // Here's an example of a DELETE request
        .delete("/reader/12")
    )

    .pause(1)
    .exec(
      http("request_14") // Here's an example of a POST request
        .post("/")
        .formParam("author", "William Shakespeare") // Note the triple double quotes: used in Scala for protecting a whole chain of characters (no need for backslash)
        .formParam("title", "A Midsummer Night's Dream")
        .formParam("genre", "Poetry")
    )

        .pause(1)
    .exec(
      http("request_15") // Here's an example of a GET request
        .get("/12")
    )

        .pause(1)
    .exec(
      http("request_16") // Here's an example of a DELETE request
        .delete("/13")
    )

  setUp(scn.inject(atOnceUsers(1)).protocols(httpProtocol))
}
