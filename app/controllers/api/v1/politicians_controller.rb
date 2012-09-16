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

          i = 0
          @issue_names.each do |n|
            res[i] = Hash.new
            res[i]["issue name"] = n
            res[i][@white.name] = @white.issues.first(:name => n).stance
            res[i][@black.name] = @black.issues.first(:name => n).stance
            res[i]["color"] = "blue"
            i = i + 1
          end

          respond_with res.to_a
        end
      end
    end
  end
end