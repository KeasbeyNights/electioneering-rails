ElectioneeringRails::Application.routes.draw do
  match "compare" => "home#compare"
  match "admin" => "admin#index"
  match "create" => "admin#create"

  namespace :api, defaults: {format: 'json'} do
    namespace :v1 do
      resources :politicians
    end
  end

  root :to => 'home#index'
end
