#!/usr/bin/env ambari-python-wrap
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

class HDP23StackAdvisor(HDP22StackAdvisor):

  def getServiceConfigurationRecommenderDict(self):
    parentRecommendConfDict = super(HDP23StackAdvisor, self).getServiceConfigurationRecommenderDict()
    childRecommendConfDict = {
      "TEZ": self.recommendTezConfigurations,
    }
    parentRecommendConfDict.update(childRecommendConfDict)
    return parentRecommendConfDict

  def recommendTezConfigurations(self, configurations, clusterData, services, hosts):
    super(HDP23StackAdvisor, self).recommendTezConfigurations(configurations, clusterData, services, hosts)
    if "tez-site" in services["configurations"] and "tez.runtime.sorter.class" in services["configurations"]["tez-site"]["properties"]:
      if services["configurations"]["tez-site"]["properties"]["tez.runtime.sorter.class"] == "LEGACY":
        putTezAttribute = self.putPropertyAttribute(configurations, "tez-site")
        putTezAttribute("tez.runtime.io.sort.mb","maximum", 2047)