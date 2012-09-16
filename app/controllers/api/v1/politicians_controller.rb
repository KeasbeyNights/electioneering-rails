module Api
  module V1
    class PoliticiansController < ApplicationController
      respond_to :json

      def index
        if !params["names"]["auth"].eql?('lZvqvJZgXVsYVB43siOl0jsAYNhJXR3Qhnyh4tQlEgSxRi1qxuG7qtXDqjOTk4KN')
          respond_with ''
        elsif params["names"]["white"].nil? || 
          params["names"]["black"].nil?
          respond_with Politician.all
        else
          @white = Politician.where(:name => params["names"]["white"]).first
          @black = Politician.where(:name => params["names"]["black"]).first

          res = Hash.new
          @issue_names = @white.issues.map { |x| x.name } & 
            @black.issues.map { |x| x.name }

          str = ""

          @issue_names.each do |n|
            @w_issue = @white.issues.first(:name => n)
            @b_issue = @black.issues.first(:name => n)
            res[""] = Hash.new
            res[""]["issueName"] = n
            res[""]["whiteStance"] = @w_issue.stance
            res[""]["blackStance"] = @b_issue.stance
            res[""]["color"] = @w_issue.colorize(@b_issue)
            str << res.to_a.to_s.gsub(/\["", /, "").gsub(/\]\]/, "]").
            gsub(/=>/, ":")
          end

          respond_with str.gsub(/\]\[/, ", ").gsub(/", "/, "\",\"").gsub(/}, {/, "\},\{")
        end
      end
    end
  end
end