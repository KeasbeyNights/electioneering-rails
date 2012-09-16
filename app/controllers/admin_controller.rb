class AdminController < ApplicationController
  def index
    @politician = Politician.new
  end

  def create
    @politician = Politician.new(:name => params[:name], 
      :party => params[:party], 
      :candidate_type => params[:candidate_type]
    )
    @politician.save!

    @issues = ["abortion", "education", "energy", "entitlements", 
      "foreign_middle_east", "foreign_europe_asia", "foreign_rest", 
      "gay_marriage", "gun_policy", "healthcare", "immigration", 
      "jobs", "taxes", "special_interest"]
    name_mapper = Hash[
      "abortion" => "Abortion", 
      "education" => "Education", 
      "energy" => "Energy", 
      "entitlements" => "Entitlements", 
      "foreign_middle_east" => "Foreign Policy - Middle East", 
      "foreign_europe_asia" => "Foreign Policy - Europe / Asia", 
      "foreign_rest" => "Foreign Policy - Rest of World", 
      "gay_marriage" => "Gay Marriage", 
      "gun_policy" => "Gun Policy", 
      "healthcare" => "Health Care",
      "immigration" => "Immigration", 
      "jobs" => "Jobs", 
      "taxes" => "Taxes", 
      "special_interest" => "Special Interest"
    ]
    params.to_a.each do |param|
      if @issues.include?(param[0])
        @issue = Issue.new(
          :name => name_mapper[param[0]], 
          :stance => param[1], 
          :politician_id => @politician._id
        )
        @issue.save!
      end
    end
    redirect_to '/admin'
  end
end